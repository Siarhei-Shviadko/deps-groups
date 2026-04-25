from typing import TypedDict

__all__ = ["DocumentTypeInfo"]


class DocumentTypeInfo(TypedDict):
    document_type_id: str
    tenant_id: str
