from pydantic import Field

from deps_groups.domain.model import NAME_MAX_LENGTH

from ..configured_base_serializer import ConfiguredRequestSerializer

__all__ = ["UpdateGroupInfoRequest"]


class UpdateGroupInfoRequest(ConfiguredRequestSerializer):
    name: str = Field(..., min_length=1, max_length=NAME_MAX_LENGTH)
