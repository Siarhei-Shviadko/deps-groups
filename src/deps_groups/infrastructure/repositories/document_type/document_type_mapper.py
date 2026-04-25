from typing import Any

from deps_groups.domain.model import DocumentType

__all__ = ["DocumentTypeMapper"]


class DocumentTypeMapper:
    @staticmethod
    def to_dict(document_type: DocumentType) -> dict[str, Any]:
        return {
            "document_type_id": document_type.id(),
            "tenant_id": document_type.tenant_id(),
        }

    @staticmethod
    def from_dict(document_type: dict[str, Any]) -> DocumentType:
        return DocumentType(
            id_=document_type["document_type_id"],
            tenant_id=document_type["tenant_id"],
        )
