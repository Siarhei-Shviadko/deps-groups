from sqlalchemy import Column, String, Table

from deps_groups.extras import metadata

__all__ = ["document_type_table"]


document_type_table = Table(
    "document_type",
    metadata,
    Column("document_type_id", String, primary_key=True),
    Column("tenant_id", String, nullable=False),
)
