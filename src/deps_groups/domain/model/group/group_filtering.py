from dataclasses import dataclass
from datetime import datetime
from typing import Optional

__all__ = ["GroupFiltering"]


@dataclass
class GroupFiltering:
    tenant_id: Optional[str] = None
    name: Optional[str] = None
    is_deleted: Optional[bool] = None
    document_type_id: Optional[str] = None
    datetime_range: Optional[tuple[datetime, datetime]] = None
