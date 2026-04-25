from pydantic import Field

from deps_groups.domain.model import GroupDetailsInfo

from ..configured_base_serializer import ConfiguredResponseSerializer

__all__ = ["GetGroupResponse"]


class GroupDetailsSerializer(ConfiguredResponseSerializer):
    id: str
    name: str
    document_type_ids: list[str] = Field(..., alias="documentTypeIds")

    @classmethod
    def from_domain(cls, group: GroupDetailsInfo) -> "GroupDetailsSerializer":
        return cls(
            id=group["id"],
            name=group["name"],
            document_type_ids=group["document_type_ids"],
        )


class GetGroupResponse(ConfiguredResponseSerializer):
    group: GroupDetailsSerializer

    @classmethod
    def from_domain(cls, group: GroupDetailsInfo) -> "GetGroupResponse":
        return cls(group=GroupDetailsSerializer.from_domain(group))
