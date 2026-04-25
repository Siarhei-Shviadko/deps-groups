from datetime import datetime
from uuid import uuid4

from .group import Group
from .group_created import GroupCreated

__all__ = ["GroupFactory"]


class GroupFactory:
    @classmethod
    def create(cls, tenant_id: str, name: str, document_types: list[str]) -> Group:
        group_id = uuid4().hex

        return Group(
            id_=group_id,
            tenant_id=tenant_id,
            name=name,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            document_types=document_types,
            events=[
                GroupCreated(
                    id=group_id,
                    tenant_id=tenant_id,
                    name=name,
                    document_type_ids=document_types,
                ),
            ],
        )
