from typing import TypedDict

from ..shared import PaginatedResultMetadataInfo

__all__ = ["GroupInfo", "ShortGroupInfo", "GroupsInfo", "GroupListMetadataInfo", "GroupDetailsInfo"]


class GroupInfo(TypedDict):
    id: str
    tenant_id: str
    name: str
    created_at: str
    updated_at: str
    document_type_ids: list[str]
    is_deleted: bool


class GroupDetailsInfo(TypedDict):
    id: str
    name: str
    document_type_ids: list[str]


class ShortGroupInfo(TypedDict):
    id: str
    tenant_id: str
    name: str
    document_type_ids: list[str]
    is_deleted: bool


class GroupListMetadataInfo(PaginatedResultMetadataInfo):
    pass


class GroupsInfo(TypedDict):
    groups: list[GroupInfo]
    metadata: GroupListMetadataInfo
