from deps_groups.domain.model import PaginatedResultMetadataInfo

from ..configured_base_serializer import ConfiguredResponseSerializer

__all__ = [
    "PaginatedResultMetadataSerializer",
]


class PaginatedResultMetadataSerializer(ConfiguredResponseSerializer):
    size: int
    total: int

    @classmethod
    def from_domain(cls, metadata: PaginatedResultMetadataInfo) -> "PaginatedResultMetadataSerializer":
        return cls(
            size=metadata["size"],
            total=metadata["total"],
        )
