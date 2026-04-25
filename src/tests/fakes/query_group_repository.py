from typing import Optional

from deps_groups.domain.model import (
    Group,
    GroupDetailsInfo,
    IQueryGroupRepository,
    ShortGroupInfo,
)


class FakeQueryGroupRepository(IQueryGroupRepository):
    def __init__(self):
        self._db: dict[(str, str), Group] = {}

    def clear(self):
        self._db.clear()

    def find(self, group_id: str, tenant_id: str) -> Optional[GroupDetailsInfo]:
        group = self._db.get((group_id, tenant_id))

        return (
            GroupDetailsInfo(
                id=group.id(),
                name=group.name,
                document_type_ids=[dt_id() for dt_id in group.document_types],
            )
            if group is None or (group is not None and group.is_deleted)
            else None
        )

    def find_all(self) -> list[ShortGroupInfo]:
        sorted_groups = sorted(self._db.values(), key=lambda group: group.created_at, reverse=True)

        return [
            ShortGroupInfo(
                id=group.id(),
                tenant_id=group.tenant_id(),
                name=group.name,
                document_type_ids=[dt_id() for dt_id in group.document_types],
                is_deleted=group.is_deleted,
            )
            for group in sorted_groups
        ]
