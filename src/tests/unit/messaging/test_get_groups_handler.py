import json

from deps_message_flow.commands.consumer import CommandMessage

from deps_groups.constants import DOCUMENT_COMMANDS_REPLIES
from deps_groups.domain.model import Group, IQueryGroupRepository
from deps_groups.messaging import GetGroupsReply
from deps_groups.messaging.handlers import get_groups_handler


def test_get_groups_handler__for_document(
    group_1: Group,
    group_2: Group,
    get_groups_command_message__document: CommandMessage,
    fake_query_group_repository: IQueryGroupRepository,
):
    fake_query_group_repository._db = {
        (group_1.id(), group_1.tenant_id()): group_1,
        (group_2.id(), group_2.tenant_id()): group_2,
    }

    message = get_groups_handler(get_groups_command_message__document)[0]

    expected_payload = {
        "groups": [
            {
                "id": group_2.id(),
                "tenant_id": group_2.tenant_id(),
                "name": group_2.name,
                "document_type_ids": [dt_id() for dt_id in group_2.document_types],
                "is_deleted": group_2.is_deleted,
            },
            {
                "id": group_1.id(),
                "tenant_id": group_1.tenant_id(),
                "name": group_1.name,
                "document_type_ids": [dt_id() for dt_id in group_1.document_types],
                "is_deleted": group_1.is_deleted,
            },
        ]
    }

    assert message.payload == json.dumps(expected_payload).encode()
    assert message.headers["command_destination"] == DOCUMENT_COMMANDS_REPLIES
    assert message.headers["command_type"] == GetGroupsReply.__name__
    assert message.headers["reply_outcome_type"] == "SUCCESS"
