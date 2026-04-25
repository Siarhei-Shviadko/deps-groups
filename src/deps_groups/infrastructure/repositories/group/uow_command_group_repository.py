from sqlalchemy import Column, and_, delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from deps_groups.domain.model import Group, ICommandGroupRepository

from ..tables import group_document_types_table, group_table
from .group_mapper import GroupMapper, GroupsMapper

__all__ = ["UoWCommandGroupRepository"]


class UoWCommandGroupRepository(ICommandGroupRepository):  # noqa: WPS214
    def __init__(self, connection: Session) -> None:
        self._connection = connection

    @property
    def group_table(self) -> list[Column]:
        return [
            group_table.c.group_id,
            group_table.c.tenant_id,
            group_table.c.name,
            group_table.c.created_at,
            group_table.c.updated_at,
            group_table.c.is_deleted,
            group_document_types_table.c.document_type_id,
        ]

    @property
    def joined_tables(self) -> list[Column]:
        return group_table.outerjoin(
            group_document_types_table,
            group_document_types_table.c.group_id == group_table.c.group_id,
        )

    def group_of_id(self, group_id: str, tenant_id: str) -> Group | None:
        query = (
            select(self.group_table)
            .select_from(self.joined_tables)
            .where(
                and_(
                    group_table.c.group_id == group_id,
                    group_table.c.tenant_id == tenant_id,
                    group_table.c.is_deleted == False,  # noqa: E712
                ),
            )
        )

        rows = self._connection.execute(query)

        if rows.rowcount < 1:
            return None

        return GroupMapper.from_dict(rows.fetchall())

    def groups_of_ids(self, groups_ids: list[str], tenant_id: str) -> list[Group]:
        query = (
            select(self.group_table)
            .select_from(self.joined_tables)
            .where(
                and_(
                    group_table.c.group_id.in_(groups_ids),
                    group_table.c.tenant_id == tenant_id,
                    group_table.c.is_deleted == False,  # noqa: E712
                ),
            )
            .order_by(group_table.c.created_at)
        )

        rows = self._connection.execute(query).fetchall()

        return GroupsMapper.from_dict(rows)

    def save(self, group: Group) -> None:
        self._save_group(group)
        self._save_document_types(group)

    def has_group_with_name(self, name: str, tenant_id: str) -> bool:
        query = select([group_table.c.group_id]).where(
            and_(
                group_table.c.name == name,
                group_table.c.tenant_id == tenant_id,
            ),
        )

        result = self._connection.execute(query).fetchone()

        return result is not None

    def delete_all(self, groups: list[Group]) -> None:
        for group in groups:
            self.save(group)

    def erase_all_groups(self) -> None:
        self._connection.execute(delete(group_table))

    def _save_group(self, group: Group) -> None:
        save_command = (
            insert(group_table)
            .on_conflict_do_update(
                index_elements=[group_table.c.group_id],
                set_=GroupMapper.to_dict(group),
            )
            .values(**GroupMapper.to_dict(group))
        )

        self._connection.execute(save_command)

    def _save_document_types(self, group: Group) -> None:
        if group.document_types:
            save_document_types = (
                insert(group_document_types_table)
                .on_conflict_do_nothing()
                .values(
                    [
                        {"group_id": group.id(), "document_type_id": document_type_id()}
                        for document_type_id in group.document_types
                    ],
                )
            )

            delete_document_types = delete(group_document_types_table).where(
                and_(
                    group_document_types_table.c.group_id == group.id(),
                    group_document_types_table.c.document_type_id.notin_([dt() for dt in group.document_types]),
                ),
            )

            self._connection.execute(save_document_types)
            self._connection.execute(delete_document_types)
        else:
            delete_all_document_types = delete(group_document_types_table).where(
                group_document_types_table.c.group_id == group.id(),
            )

            self._connection.execute(delete_all_document_types)
