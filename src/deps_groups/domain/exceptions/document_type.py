from .base import NotFoundError

__all__ = ["DocumentTypeNotFound"]


class DocumentTypeNotFound(NotFoundError):
    code = "document_type_not_found"

    def __init__(self, document_type_id: str) -> None:
        super().__init__(f"DocumentType with id `{document_type_id}` not found.")
