from typing import Any, Mapping

from deps_groups.domain.model import (
    GroupDetailsInfo,
    GroupInfo,
    GroupListMetadataInfo,
    GroupsInfo,
    ShortGroupInfo,
)

Row = Mapping[str, Any]


__all__ = ["GroupsInfoMapper", "GroupInfoMapper"]


class GroupsInfoMapper:
    @classmethod
    def from_group_rows(cls, rows: list[Row], total: int) -> GroupsInfo:
        return GroupsInfo(
            groups=[GroupInfoMapper.from_group_row(row) for row in rows],
            metadata=GroupListMetadataInfo(
                size=len(rows),
                total=total,
            ),
        )

    @classmethod
    def from_short_group_rows(cls, rows: list[Row]) -> list[ShortGroupInfo]:
        return [GroupInfoMapper.from_short_group_row(row) for row in rows]


class GroupInfoMapper:
    @staticmethod
    def from_group_row(row: Row) -> GroupInfo:
        return GroupInfo(
            id=row["id"],
            tenant_id=row["tenant_id"],
            name=row["name"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            document_type_ids=row["document_type_ids"] or [],
            is_deleted=row["is_deleted"],
        )

    @staticmethod
    def from_short_group_row(row: Row) -> ShortGroupInfo:
        return ShortGroupInfo(
            id=row["id"],
            tenant_id=row["tenant_id"],
            name=row["name"],
            document_type_ids=row["document_type_ids"] or [],
            is_deleted=row["is_deleted"],
        )

    @staticmethod
    def from_group_detail_row(row: Row) -> GroupDetailsInfo:
        return GroupDetailsInfo(
            id=row["id"],
            name=row["name"],
            document_type_ids=row["document_type_ids"] or [],
        )
