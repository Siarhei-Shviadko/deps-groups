import logging

from dependency_injector.wiring import Provide, inject
from deps_message_flow.commands.common import (
    CommandMessageHeaders,
    CommandReplyOutcome,
    ReplyMessageHeaders,
    make_message_for_command,
)
from deps_message_flow.commands.consumer import (
    CommandHandlerReplyBuilder,
    CommandMessage,
)
from deps_message_flow.events.mappers import JsonMapper
from deps_message_flow.events.subscriber.domain_event_envelope import (
    DomainEventEnvelope,
)

from deps_groups.application import DocumentTypeService, QueryGroupService
from deps_groups.containers import Containers
from deps_groups.messaging.commands import GetGroupsReply

logger = logging.getLogger(__name__)


def is_command_successful(command_message: CommandMessage) -> bool:
    return (
        command_message.message.get_required_header(ReplyMessageHeaders.REPLY_OUTCOME)
        == CommandReplyOutcome.SUCCESS.name
    )


@inject
def document_type_created_handler(
    dee: DomainEventEnvelope,
    document_type_service: DocumentTypeService = Provide[Containers.document_type_service],
):
    document_type_service.create(document_type_id=dee.event.document_type, tenant_id=dee.event.tenant)


@inject
def document_type_deleted_handler(
    dee: DomainEventEnvelope,
    document_type_service: DocumentTypeService = Provide[Containers.document_type_service],
):
    document_type_service.delete(document_type_id=dee.event.document_type, tenant_id=dee.event.tenant)


@inject
def get_document_types_reply_handler(  # noqa: WPS463
    command_message: CommandMessage,
    document_type_service: DocumentTypeService = Provide[Containers.document_type_service],
):
    if is_command_successful(command_message):
        document_types = command_message.command.document_types
        document_type_service.save_all(document_types)
    else:
        logger.error(f"Failed to get document types. Command headers: {command_message.message.headers}")


@inject
def get_groups_handler(  # noqa: WPS463
    command_message: CommandMessage,
    query_group_service: QueryGroupService = Provide[Containers.query_group_service],
):
    replies_channel = command_message.message.headers.get(CommandMessageHeaders.REPLY_TO)

    try:
        command_reply = GetGroupsReply(groups=query_group_service.find_all())

        message_reply = make_message_for_command(
            replies_channel,
            JsonMapper().serialize(command_reply),
            command_reply.__class__.__name__,
            "NONE",
        )

        return [CommandHandlerReplyBuilder.with_success(message_reply)]

    except Exception as e:
        command_reply = GetGroupsReply([])
        message_reply = make_message_for_command(
            replies_channel,
            JsonMapper().serialize(command_reply),
            command_reply.__class__.__name__,
            "NONE",
        )

        logger.error(f"Failed to get groups! \n Reason: {e}")

        return [CommandHandlerReplyBuilder.with_failure(message_reply)]
