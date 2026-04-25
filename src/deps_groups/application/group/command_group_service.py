import logging

from deps_message_flow.events.publisher import DomainEventPublisher

from deps_groups.constants import GROUP_DESTINATION
from deps_groups.domain.exceptions import (
    DocumentTypesNotFound,
    GroupNotFound,
    GroupWithNameAlreadyExists,
)
from deps_groups.domain.model import Group, GroupFactory
from deps_groups.infrastructure.unit_of_work import AbstractUnitOfWork

from ..retry_transaction import retry_on_transaction_error

__all__ = ["CommandGroupService"]


class CommandGroupService:
    def __init__(
        self,
        unit_of_work: AbstractUnitOfWork,
        domain_event_publisher: DomainEventPublisher,
    ) -> None:
        self._uow = unit_of_work
        self._domain_event_publisher = domain_event_publisher

        self._logger = logging.getLogger(self.__class__.__name__)

    @retry_on_transaction_error()
    def create(self, tenant_id: str, name: str, document_type_ids: list[str]) -> Group:
        group = GroupFactory.create(tenant_id=tenant_id, name=name, document_types=document_type_ids)

        with self._uow:
            self._check_group_name(name, tenant_id)
            self._check_document_types(document_type_ids, tenant_id)

            self._uow.groups.save(group)
            self._uow.commit()

            self._publish_events(group)

        self._logger.info("Group with id `%s` is saved.", group.id())

        return group

    @retry_on_transaction_error()
    def update_info(self, id_: str, tenant_id: str, name: str) -> Group:
        with self._uow:
            group = self._find_group(id_, tenant_id)

            if group.name != name:
                self._check_group_name(name, tenant_id)

            group.update_info(name=name)

            self._uow.groups.save(group)
            self._uow.commit()

            self._publish_events(group)

        self._logger.info("Group with id `%s` is updated.", group.id())

        return group

    @retry_on_transaction_error()
    def delete(self, ids: list[str], tenant_id: str) -> list[Group]:
        with self._uow:
            groups = self._uow.groups.groups_of_ids(ids, tenant_id)

            for group in groups:
                group.delete()

            self._uow.groups.delete_all(groups)
            self._uow.commit()

            for group in groups:
                self._publish_events(group)

        self._logger.info("Groups with ids `%s` are deleted.", ids)

        return groups

    @retry_on_transaction_error()
    def add_document_types(self, id_: str, tenant_id: str, document_types_ids: list[str]) -> Group:
        with self._uow:
            self._check_document_types(document_types_ids, tenant_id)
            group = self._find_group(id_, tenant_id)

            group.add_document_types(document_types_ids)

            self._uow.groups.save(group)
            self._uow.commit()

            self._publish_events(group)

        self._logger.info("Document Types `%s` are added to Group %s.", document_types_ids, id_)

        return group

    @retry_on_transaction_error()
    def remove_document_types(self, id_: str, tenant_id: str, document_types_ids: list[str]) -> Group:
        with self._uow:
            group = self._find_group(id_, tenant_id)

            group.remove_document_types(document_types_ids)

            self._uow.groups.save(group)
            self._uow.commit()

            self._publish_events(group)

        self._logger.info("Document Types `%s` are removed from Group %s.", document_types_ids, id_)

        return group

    def _check_group_name(self, name: str, tenant_id: str) -> None:
        if self._uow.groups.has_group_with_name(name, tenant_id):
            raise GroupWithNameAlreadyExists(name)

    def _check_document_types(self, document_type_ids: list[str], tenant_id: str) -> None:
        invalid_document_types = self._uow.document_types.document_types_of_invalid_ids(document_type_ids, tenant_id)

        if invalid_document_types:
            raise DocumentTypesNotFound(invalid_document_types)

    def _find_group(self, id_: str, tenant_id: str) -> Group:
        if (group := self._uow.groups.group_of_id(id_, tenant_id)) is None:
            raise GroupNotFound(group_id=id_, tenant_id=tenant_id)

        return group

    def _publish_events(self, group: Group) -> None:
        self._domain_event_publisher.publish(
            aggregate_type=GROUP_DESTINATION,
            aggregate_id=group.id(),
            domain_events=group.events,
        )
