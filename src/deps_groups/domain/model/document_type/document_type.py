from ..shared import Event, Guard, ImmutableCheck, TenantId
from .document_type_id import DocumentTypeId

__all__ = ["DocumentType"]


class DocumentType:
    id = Guard[DocumentTypeId](DocumentTypeId, ImmutableCheck())
    tenant_id = Guard[TenantId](TenantId, ImmutableCheck())

    def __init__(
        self,
        id_: str,
        tenant_id: str,
        *,
        events: list[Event] | None = None,
    ) -> None:
        self.id = DocumentTypeId(id_)
        self.tenant_id = TenantId(tenant_id)

        self.events = events or []

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and other.id == self.id

    def __repr__(self) -> str:
        return "\n".join(
            (
                f"<class '{self.__class__.__name__}':",
                f"{self.id = },",
                f"{self.tenant_id = },",
            ),
        )

    def delete(self) -> None:
        pass
