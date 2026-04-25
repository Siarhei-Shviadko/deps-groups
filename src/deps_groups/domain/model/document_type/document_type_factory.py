from .document_type import DocumentType

__all__ = ["DocumentTypeFactory"]


class DocumentTypeFactory:
    @classmethod
    def create(cls, id_: str, tenant_id: str) -> DocumentType:
        return DocumentType(
            id_=id_,
            tenant_id=tenant_id,
        )
