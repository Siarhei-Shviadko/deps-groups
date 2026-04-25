from typing import Optional, Protocol

from ..shared import Pagination
from .group_filtering import GroupFiltering
from .group_info import GroupDetailsInfo, GroupsInfo, ShortGroupInfo
from .group_sorting import GroupSorting

__all__ = ["IQueryGroupRepository"]


class IQueryGroupRepository(Protocol):
    def find(self, group_id: str, tenant_id: str) -> Optional[GroupDetailsInfo]:
        pass

    def find_all(self) -> list[ShortGroupInfo]:
        pass

    def find_all_with(
        self,
        filtering: Optional[GroupFiltering] = None,
        sorting: Optional[GroupSorting] = None,
        pagination: Optional[Pagination] = None,
    ) -> GroupsInfo:
        pass
