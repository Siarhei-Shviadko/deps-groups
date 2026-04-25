from datetime import datetime

from deps_groups.domain.exceptions import DocumentTypesLimitExceeded, IllegalArgument

from ..shared import EntityId, Event, Guard, ImmutableCheck, LengthCheck, TenantId
from .document_type_added import DocumentTypesAdded
from .document_type_removed import DocumentTypesRemoved
from .group_deleted import GroupDeleted
from .group_info_updated import GroupInfoUpdated

__all__ = ["Group", "MAX_DOCUMENT_TYPES", "MIN_DOCUMENT_TYPES", "NAME_MAX_LENGTH"]

NAME_MAX_LENGTH = 100
MAX_DOCUMENT_TYPES = 25
MIN_DOCUMENT_TYPES = 0


class Group:  # noqa: WPS230
    id = Guard[EntityId](EntityId, ImmutableCheck())
    tenant_id = Guard[TenantId](TenantId, ImmutableCheck())
    name = Guard[str](str, LengthCheck(max_length=NAME_MAX_LENGTH))
    created_at = Guard[datetime](datetime, ImmutableCheck())
    updated_at = Guard[datetime](datetime)
    is_deleted = Guard[bool](bool)

    _document_types = Guard[list[EntityId]](
        list,
        LengthCheck(min_length=MIN_DOCUMENT_TYPES, max_length=MAX_DOCUMENT_TYPES),
    )

    def __init__(
        self,
        id_: str,
        tenant_id: str,
        name: str,
        created_at: datetime,
        updated_at: datetime,
        *,
        document_types: list[str] | None = None,
        is_deleted: bool = False,
        events: list[Event] | None = None,
    ) -> None:
        self.id = EntityId(id_)
        self.tenant_id = TenantId(tenant_id)
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at

        self.document_types = [EntityId(document_type) for document_type in document_types] if document_types else []
        self.is_deleted = is_deleted

        self.events = events or []

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and other.id == self.id

    def __repr__(self) -> str:
        return "\n".join(
            (
                f"<class '{self.__class__.__name__}':",
                f"{self.id = },",
                f"{self.tenant_id = },",
                f"{self.name = },",
                f"{self.created_at = },",
                f"{self.updated_at = },",
                f"{self.document_types = }, >",
                f"{self.is_deleted = }>",
            ),
        )

    @property
    def document_type_ids(self) -> set[str]:
        return {document_type_id() for document_type_id in self.document_types}

    @property
    def document_types(self) -> list[EntityId]:
        return self._document_types

    @document_types.setter
    def document_types(self, document_types: list[EntityId]) -> None:
        try:
            self._document_types = document_types
        except IllegalArgument:
            raise DocumentTypesLimitExceeded(MAX_DOCUMENT_TYPES)

    def update_info(self, name: str) -> None:
        self.name = name

        self.updated_at = datetime.now()

        self.events.append(
            GroupInfoUpdated(
                id=self.id(),
                tenant_id=self.tenant_id(),
                name=name,
            ),
        )

    def delete(self) -> None:
        self.is_deleted = True
        self.updated_at = datetime.now()

        self.events.append(
            GroupDeleted(
                id=self.id(),
                tenant_id=self.tenant_id(),
            ),
        )

    def add_document_types(self, document_types_ids: list[str]) -> None:
        new_document_types = [
            EntityId(document_type_id)
            for document_type_id in document_types_ids
            if document_type_id not in self.document_type_ids
        ]

        if not new_document_types:
            return

        self.document_types = [*self.document_types, *new_document_types]

        self.updated_at = datetime.now()

        self.events.append(
            DocumentTypesAdded(
                id=self.id(),
                tenant_id=self.tenant_id(),
                document_type_ids=[dt() for dt in new_document_types],
            ),
        )

    def remove_document_types(self, document_types_ids: list[str]) -> None:
        removed_document_types = []

        for document_type_id in document_types_ids:
            if (entity_id := EntityId(document_type_id)) in self.document_types:
                self.document_types.remove(entity_id)
                removed_document_types.append(document_type_id)

        self.updated_at = datetime.now()

        if removed_document_types:
            self.events.append(
                DocumentTypesRemoved(
                    id=self.id(),
                    tenant_id=self.tenant_id(),
                    document_type_ids=removed_document_types,
                ),
            )
