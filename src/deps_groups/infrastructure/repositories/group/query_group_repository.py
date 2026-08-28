from functools import cached_property
from typing import Optional

from sqlalchemy import Column, and_, asc, desc, func, select
from sqlalchemy.sql.selectable import CTE, Select

from deps_groups.domain.model import (
    GroupDetailsInfo,
    GroupFiltering,
    GroupsInfo,
    GroupSortBy,
    GroupSorting,
    IQueryGroupRepository,
    Pagination,
    ShortGroupInfo,
    SortOrder,
)
from deps_groups.extras import DatabaseSession

from ..tables import group_document_types_table, group_table
from .group_info_mapper import GroupInfoMapper, GroupsInfoMapper

__all__ = ["QueryGroupRepository"]


class QueryGroupRepository(IQueryGroupRepository):
    GROUP_ID_ALIAS = "id"

    def __init__(self, database: DatabaseSession) -> None:
        self._db = database

    @cached_property
    def document_type_ids_cte(self) -> CTE:
        return (
            select(
                group_document_types_table.c.group_id,
                func.coalesce(
                    func.json_agg(
                        group_document_types_table.c.document_type_id,
                    ),
                    "[]",
                ).label("document_type_ids"),
            )
            .select_from(group_document_types_table)
            .group_by(group_document_types_table.c.group_id)
            .cte("group_document_type_ids")
        )

    @cached_property
    def joined_group_tables(self) -> list[Column]:
        return group_table.outerjoin(
            self.document_type_ids_cte,
            self.document_type_ids_cte.c.group_id == group_table.c.group_id,
        )

    def find(self, group_id: str, tenant_id: str) -> Optional[GroupDetailsInfo]:
        query = (
            select(
                group_table.c.group_id.label(self.GROUP_ID_ALIAS),
                group_table.c.name,
                self.document_type_ids_cte,
            )
            .select_from(
                self.joined_group_tables,
            )
            .where(
                and_(
                    group_table.c.group_id == group_id,
                    group_table.c.tenant_id == tenant_id,
                    group_table.c.is_deleted == False,  # noqa: E712
                ),
            )
        )

        with self._db.connection() as conn:
            row = conn.execute(query).mappings().first()

        return GroupInfoMapper.from_group_detail_row(row) if row else None

    def find_all(self) -> list[ShortGroupInfo]:
        query = select(
            group_table.c.group_id.label(self.GROUP_ID_ALIAS),
            group_table.c.tenant_id,
            group_table.c.name,
            group_table.c.is_deleted,
            self.document_type_ids_cte,
        ).select_from(self.joined_group_tables)

        query = self._apply_sorting(query)

        with self._db.connection() as conn:
            return GroupsInfoMapper.from_short_group_rows(conn.execute(query).mappings().all())

    def find_all_with(
        self,
        filtering: Optional[GroupFiltering] = None,
        sorting: Optional[GroupSorting] = None,
        pagination: Optional[Pagination] = None,
    ) -> GroupsInfo:
        query = select(
            group_table.c.group_id.label(self.GROUP_ID_ALIAS),
            group_table.c.tenant_id,
            group_table.c.name,
            group_table.c.created_at,
            group_table.c.updated_at,
            group_table.c.is_deleted,
            self.document_type_ids_cte,
        ).select_from(
            group_table.outerjoin(
                self.document_type_ids_cte,
                self.document_type_ids_cte.c.group_id == group_table.c.group_id,
            ),
        )

        total_query = select(func.count()).select_from(group_table)

        if filtering:
            query = self._apply_filtering(query, filtering)
            total_query = self._apply_filtering(total_query, filtering)

        query = self._apply_sorting(query, sorting)

        if pagination:
            query = self._apply_pagination(query, pagination)

        with self._db.connection() as conn:
            total = conn.execute(total_query).scalar()

            return GroupsInfoMapper.from_group_rows(conn.execute(query).mappings().all(), total)

    def _apply_filtering(self, query: Select, filtering: GroupFiltering) -> Select:
        if filtering.tenant_id is not None:
            query = query.where(group_table.c.tenant_id == filtering.tenant_id)

        if filtering.name is not None:
            query = query.where(group_table.c.name.ilike(f"%{filtering.name}%"))

        if filtering.is_deleted is not None:
            query = query.where(group_table.c.is_deleted == filtering.is_deleted)

        if filtering.datetime_range is not None:
            start_dt, end_dt = filtering.datetime_range
            query = query.where(group_table.c.created_at.between(start_dt, end_dt))

        if filtering.document_type_id:
            subquery = select(
                func.json_array_elements_text(self.document_type_ids_cte.c.document_type_ids).label(
                    "document_type",
                ),
                self.document_type_ids_cte.c.group_id,
            ).alias("document_type_elements")

            query = query.where(
                and_(
                    subquery.c.document_type.in_([filtering.document_type_id]),
                    subquery.c.group_id == group_table.c.group_id,
                ),
            )

        return query

    def _apply_sorting(self, query: Select, sorting: Optional[GroupSorting] = None) -> Select:
        sorting = sorting or GroupSorting()

        sort_by_to_column_mapping = {
            GroupSortBy.CREATED_AT: group_table.c.created_at,
            GroupSortBy.NAME: group_table.c.name,
        }

        order_func = asc if sorting.sort_order == SortOrder.ASC else desc

        if (sort_by_column := sort_by_to_column_mapping.get(sorting.sort_by)) is not None:
            query = query.order_by(order_func(sort_by_column))

        return query

    def _apply_pagination(self, query: Select, pagination: Pagination) -> Select:
        return query.limit(pagination.per_page).offset(pagination.offset)
