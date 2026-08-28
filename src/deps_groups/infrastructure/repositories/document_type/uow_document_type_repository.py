from sqlalchemy import Column, and_, delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from deps_groups.domain.model import DocumentType, IDocumentTypeRepository

from ..tables import document_type_table
from .document_type_mapper import DocumentTypeMapper

__all__ = ["UoWDocumentTypeRepository"]


class UoWDocumentTypeRepository(IDocumentTypeRepository):
    def __init__(self, connection: Session) -> None:
        self._connection = connection

    @property
    def document_type_columns(self) -> list[Column]:
        return [
            document_type_table.c.document_type_id,
            document_type_table.c.tenant_id,
        ]

    def document_type_of_id(self, document_type_id: str, tenant_id: str) -> DocumentType | None:
        query = select(*self.document_type_columns).where(
            and_(
                document_type_table.c.document_type_id == document_type_id,
                document_type_table.c.tenant_id == tenant_id,
            ),
        )

        row = self._connection.execute(query).mappings().first()

        if row is None:
            return None

        return DocumentTypeMapper.from_dict(row)

    def document_types_of_invalid_ids(self, document_type_ids: list[str], tenant_id: str) -> list[str]:
        query = select(document_type_table.c.document_type_id).where(
            and_(
                document_type_table.c.document_type_id.in_(document_type_ids),
                document_type_table.c.tenant_id == tenant_id,
            ),
        )

        rows = self._connection.execute(query).fetchall()
        found_ids = {row.document_type_id for row in rows}

        return list(set(document_type_ids) - found_ids)

    def save_new(self, document_type: DocumentType) -> None:
        insert_query = insert(document_type_table)
        save_query = insert_query.on_conflict_do_nothing().values(**DocumentTypeMapper.to_dict(document_type))

        self._connection.execute(save_query)

    def save_all(self, document_types: list[DocumentType]) -> None:
        if not document_types:
            return

        insert_query = insert(document_type_table)
        save_query = insert_query.on_conflict_do_nothing().values(
            [DocumentTypeMapper.to_dict(document_type) for document_type in document_types],
        )

        self._connection.execute(save_query)

    def delete(self, document_type: DocumentType) -> None:
        delete_query = delete(document_type_table).where(
            and_(
                document_type_table.c.document_type_id == document_type.id(),
                document_type_table.c.tenant_id == document_type.tenant_id(),
            ),
        )
        self._connection.execute(delete_query)

    def erase_all_document_types(self) -> None:
        self._connection.execute(delete(document_type_table))
