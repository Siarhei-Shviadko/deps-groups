from pydantic import Field

from ..configured_base_serializer import ConfiguredRequestSerializer

__all__ = ["AddDocumentTypesRequest"]


class AddDocumentTypesRequest(ConfiguredRequestSerializer):
    document_types_ids: list[str] = Field(..., min_items=1, alias="documentTypeIds")
