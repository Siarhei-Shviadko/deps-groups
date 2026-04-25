from pydantic import Field

from deps_groups.domain.model import NAME_MAX_LENGTH, Group

from ..configured_base_serializer import (
    ConfiguredRequestSerializer,
    ConfiguredResponseSerializer,
)

__all__ = ["CreateGroupRequest", "CreateGroupResponse"]


class CreateGroupRequest(ConfiguredRequestSerializer):
    name: str = Field(..., min_length=1, max_length=NAME_MAX_LENGTH)
    document_type_ids: list[str] = Field(..., alias="documentTypeIds", min_length=1)


class CreateGroupResponse(ConfiguredResponseSerializer):
    id: str

    @classmethod
    def from_domain(cls, group: Group) -> "CreateGroupResponse":
        return cls(id=group.id())
