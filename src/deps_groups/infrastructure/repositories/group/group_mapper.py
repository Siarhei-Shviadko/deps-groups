from collections import defaultdict
from typing import Any, Mapping

from deps_groups.domain.model import Group

__all__ = ["GroupMapper", "GroupsMapper"]


class GroupMapper:
    @staticmethod
    def to_dict(group: Group) -> dict[str, Any]:
        return {
            "group_id": group.id(),
            "tenant_id": group.tenant_id(),
            "name": group.name,
            "created_at": group.created_at,
            "updated_at": group.updated_at,
            "is_deleted": group.is_deleted,
        }

    @staticmethod
    def from_dict(rows: list[Mapping[str, Any]]) -> Group:
        group_data = rows[0]
        return Group(
            id_=group_data["group_id"],
            tenant_id=group_data["tenant_id"],
            name=group_data["name"],
            created_at=group_data["created_at"],
            updated_at=group_data["updated_at"],
            is_deleted=group_data["is_deleted"],
            document_types=[row["document_type_id"] for row in rows] if group_data["document_type_id"] else [],
        )


class GroupsMapper:
    @staticmethod
    def from_dict(rows: list[Mapping[str, Any]]) -> list[Group]:
        rows_mapping = defaultdict(list)

        for row in rows:
            rows_mapping[row["group_id"]].append(row)

        return [GroupMapper.from_dict(rows) for rows in rows_mapping.values()]
