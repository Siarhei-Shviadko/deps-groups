from dataclasses import dataclass

from deps_message_flow.commands.common import Command

from deps_groups.domain.model import ShortGroupInfo

__all__ = ["GetGroups", "GetGroupsReply"]


class GetGroups(Command):
    pass


@dataclass
class GetGroupsReply(Command):
    groups: list[ShortGroupInfo]
