from typing import Optional, Protocol

from ..document_type import DocumentType

__all__ = ["IDocumentTypeRepository"]


class IDocumentTypeRepository(Protocol):
    def document_type_of_id(self, document_type_id: str, tenant_id: str) -> Optional[DocumentType]:
        pass

    def document_types_of_invalid_ids(self, document_type_ids: list[str], tenant_id: str) -> dict[str, bool]:
        pass

    def save_new(self, document_type: DocumentType) -> None:
        pass

    def save_all(self, document_types: list[DocumentType]) -> None:
        pass

    def delete(self, document_type: DocumentType) -> None:
        pass
