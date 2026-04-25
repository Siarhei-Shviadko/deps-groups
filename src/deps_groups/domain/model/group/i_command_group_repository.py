from typing import Protocol

from .group import Group

__all__ = ["ICommandGroupRepository"]


class ICommandGroupRepository(Protocol):
    def group_of_id(self, group_id: str, tenant_id: str) -> Group | None:
        pass

    def groups_of_ids(self, groups_ids: list[str], tenant_id: str) -> list[Group]:
        pass

    def has_group_with_name(self, name: str, tenant_id: str) -> bool:
        pass

    def save(self, group: Group) -> None:
        pass

    def delete_all(self, groups: list[Group]) -> None:
        pass
