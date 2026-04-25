import logging

from deps_message_flow.commands.producer import CommandProducer
from deps_message_flow.events.publisher import DomainEventPublisher

from deps_groups.constants import COMMANDS_CHANNEL, COMMANDS_REPLIES_CHANNEL
from deps_groups.domain.exceptions import DocumentTypeNotFound
from deps_groups.domain.model import DocumentType, DocumentTypeFactory, DocumentTypeInfo
from deps_groups.infrastructure.unit_of_work import AbstractUnitOfWork
from deps_groups.messaging.commands import GetDocumentTypes

from .retry_transaction import retry_on_transaction_error

__all__ = ["DocumentTypeService"]


class DocumentTypeService:
    def __init__(
        self,
        unit_of_work: AbstractUnitOfWork,
        command_producer: CommandProducer,
        domain_event_publisher: DomainEventPublisher,
    ) -> None:
        self._uow = unit_of_work
        self._command_producer = command_producer
        self._domain_event_publisher = domain_event_publisher

        self._logger = logging.getLogger(self.__class__.__name__)

    def obtain_all(self) -> None:
        self._command_producer.send(
            COMMANDS_CHANNEL,
            GetDocumentTypes(),
            COMMANDS_REPLIES_CHANNEL,
        )

        self._logger.info("Document Types are requested.")

    @retry_on_transaction_error()
    def save_all(self, document_types_info: list[DocumentTypeInfo]) -> list[DocumentType]:
        with self._uow:
            document_types = [
                DocumentTypeFactory.create(id_=info["document_type_id"], tenant_id=info["tenant_id"])
                for info in document_types_info
            ]

            self._uow.document_types.save_all(document_types)

            self._uow.commit()

        self._logger.info("Document Types are obtained from master source.")

        return document_types

    @retry_on_transaction_error()
    def create(self, document_type_id: str, tenant_id: str) -> DocumentType:
        with self._uow:
            document_type = DocumentTypeFactory.create(
                id_=document_type_id,
                tenant_id=tenant_id,
            )

            self._uow.document_types.save_new(document_type)

            self._uow.commit()

        self._logger.info("Document Type %s is saved.", document_type_id)

        return document_type

    @retry_on_transaction_error()
    def delete(self, document_type_id: str, tenant_id: str) -> DocumentType:
        with self._uow:
            if (document_type := self._uow.document_types.document_type_of_id(document_type_id, tenant_id)) is None:
                raise DocumentTypeNotFound(document_type_id)

            document_type.delete()

            self._uow.document_types.delete(document_type)
            self._uow.commit()

        self._logger.info("Document Type %s is deleted.", document_type_id)

        return document_type
