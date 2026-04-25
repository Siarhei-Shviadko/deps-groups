from dataclasses import dataclass

from ..shared import ExtendedEnum, SortOrder

__all__ = ["GroupSorting", "GroupSortBy"]


class GroupSortBy(ExtendedEnum):
    CREATED_AT = "createdAt"
    NAME = "name"


@dataclass
class GroupSorting:
    sort_by: GroupSortBy = GroupSortBy.CREATED_AT
    sort_order: SortOrder = SortOrder.DESC
