from dataclasses import dataclass

from deps_message_flow.commands.common import Command

from deps_groups.domain.model import DocumentTypeInfo

__all__ = ["GetDocumentTypes", "GetDocumentTypesReply"]


class GetDocumentTypes(Command):
    pass


@dataclass
class GetDocumentTypesReply(Command):
    document_types: list[DocumentTypeInfo]
