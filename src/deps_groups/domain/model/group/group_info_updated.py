from dataclasses import dataclass

from ..shared import Event

__all__ = ["GroupInfoUpdated"]


@dataclass
class GroupInfoUpdated(Event):
    id: str
    tenant_id: str
    name: str
