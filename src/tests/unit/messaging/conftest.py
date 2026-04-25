import pytest
from deps_message_flow.commands.common import CommandMessageHeaders
from deps_message_flow.commands.consumer import CommandMessage

from deps_groups.constants import DOCUMENT_COMMANDS_REPLIES


@pytest.fixture
def get_groups_command_message__document(mocker):
    cm = mocker.Mock(CommandMessage)
    cm.message.headers = {CommandMessageHeaders.REPLY_TO: DOCUMENT_COMMANDS_REPLIES}

    return cm
