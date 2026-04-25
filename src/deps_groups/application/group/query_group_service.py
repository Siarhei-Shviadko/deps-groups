import logging
from datetime import datetime
from typing import Optional

from deps_groups.domain.exceptions import GroupNotFound
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

__all__ = ["QueryGroupService"]


class QueryGroupService:
    def __init__(
        self,
        query_group_repository: IQueryGroupRepository,
        default_page: int,
        default_per_page: int,
    ) -> None:
        self._query_group_repository = query_group_repository

        self._default_page = default_page
        self._default_per_page = default_per_page

        self._logger = logging.getLogger(self.__class__.__name__)

    def find(self, group_id: str, tenant_id: str) -> GroupDetailsInfo:
        self._logger.info(f"Finding group with id {group_id} for tenant {tenant_id}...")

        if not (group := self._query_group_repository.find(group_id=group_id, tenant_id=tenant_id)):
            raise GroupNotFound(group_id=group_id, tenant_id=tenant_id)

        return group

    def find_all(self) -> list[ShortGroupInfo]:
        self._logger.info("Finding all groups...")

        return self._query_group_repository.find_all()

    def find_all_with(
        self,
        tenant_id: Optional[str] = None,
        is_deleted: Optional[bool] = None,
        name: Optional[str] = None,
        document_type_id: Optional[str] = None,
        datetime_range: Optional[tuple[datetime, datetime]] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        sort_by: GroupSortBy = GroupSortBy.CREATED_AT,
        sort_order: SortOrder = SortOrder.DESC,
    ) -> GroupsInfo:
        self._logger.info(
            f"Finding groups with filtering: {tenant_id =}, {name =}, {is_deleted =}; "
            + f"{document_type_id =}; {datetime_range =}; "
            + f"pagination: {page =}, {per_page =}; "
            + f"sorting: {sort_by =}, {sort_order =}...",
        )

        return self._query_group_repository.find_all_with(
            filtering=GroupFiltering(
                tenant_id=tenant_id,
                name=name,
                is_deleted=is_deleted,
                document_type_id=document_type_id,
                datetime_range=datetime_range,
            ),
            sorting=GroupSorting(sort_by=sort_by, sort_order=sort_order),
            pagination=Pagination(
                page=page if page is not None else self._default_page,
                per_page=per_page if per_page is not None else self._default_per_page,
            ),
        )
