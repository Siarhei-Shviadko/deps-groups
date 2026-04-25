import logging

from deps_message_flow.commands.consumer import (
    CommandDispatcher,
    CommandHandlersBuilder,
)
from deps_message_flow.events.subscriber import (
    DomainEventDispatcher,
    DomainEventHandlersBuilder,
)
from deps_message_flow.messaging.consumer import IMessageConsumer
from deps_message_flow.messaging.producer import IMessageProducer

from deps_groups.constants import (
    BATCH_COMMANDS,
    CLASSIFICATION_COMMANDS,
    COMMANDS_QUEUE,
    COMMANDS_REPLIES_CHANNEL,
    DOCUMENT_COMMANDS,
    DOCUMENT_TYPE_EXCHANGER,
    EVENTS_QUEUE,
)

from .commands import GetDocumentTypesReply, GetGroups
from .events import DocumentTypeCreated, DocumentTypeDeleted

_logger = logging.getLogger(__name__)


def make_message_dispatcher(subscriber: IMessageConsumer, producer: IMessageProducer) -> IMessageConsumer:
    from deps_groups.messaging.handlers import (  # noqa: WPS433
        document_type_created_handler,
        document_type_deleted_handler,
        get_document_types_reply_handler,
        get_groups_handler,
    )

    events_handlers = (
        DomainEventHandlersBuilder.for_aggregate_type(DOCUMENT_TYPE_EXCHANGER)
        .on_event(DocumentTypeCreated, document_type_created_handler)
        .on_event(DocumentTypeDeleted, document_type_deleted_handler)
        .for_queue(EVENTS_QUEUE)
        .build()
    )

    commands_handlers = (
        CommandHandlersBuilder.from_channel(COMMANDS_REPLIES_CHANNEL)
        .on_message(GetDocumentTypesReply, get_document_types_reply_handler)
        .and_from_channel(CLASSIFICATION_COMMANDS)
        .on_message(GetGroups, get_groups_handler)
        .and_from_channel(BATCH_COMMANDS)
        .on_message(GetGroups, get_groups_handler)
        .and_from_channel(DOCUMENT_COMMANDS)
        .on_message(GetGroups, get_groups_handler)
        .for_queue(COMMANDS_QUEUE)
        .build()
    )

    ded = DomainEventDispatcher(events_handlers, subscriber)
    ded.initialize()

    cd = CommandDispatcher(commands_handlers, subscriber, producer)
    cd.initialize()

    _logger.info("Start consuming....")

    return subscriber
