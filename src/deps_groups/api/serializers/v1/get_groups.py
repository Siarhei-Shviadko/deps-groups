from datetime import datetime
from typing import Any, Optional

from dateutil import parser
from fastapi.params import Query
from pydantic import Field, root_validator

from deps_groups.domain.model import GroupInfo, GroupsInfo, GroupSortBy, SortOrder

from ..configured_base_serializer import (
    ConfiguredRequestSerializer,
    ConfiguredResponseSerializer,
)
from .paginated_result_metadata_serializer import PaginatedResultMetadataSerializer

__all__ = ["GetGroupsRequest", "GetGroupsResponse"]


class GroupsMetadataSerializer(PaginatedResultMetadataSerializer):
    pass


class GroupSerializer(ConfiguredResponseSerializer):
    id: str
    name: str
    document_type_ids: list[str] = Field(..., alias="documentTypeIds")
    created_at: datetime = Field(..., alias="createdAt")

    @classmethod
    def from_domain(cls, group: GroupInfo) -> "GroupSerializer":
        return cls(
            id=group["id"],
            name=group["name"],
            document_type_ids=group["document_type_ids"],
            created_at=group["created_at"],
        )


class GetGroupsRequest(ConfiguredRequestSerializer):
    name: Optional[str] = Query(default=None)
    page: Optional[int] = Query(default=None, ge=0)
    document_type_id: Optional[str] = Query(default=None, alias="documentTypeId")
    date_start: Optional[str] = Query(default=None, alias="dateStart")
    date_end: Optional[str] = Query(default=None, alias="dateEnd")
    per_page: Optional[int] = Query(default=None, alias="perPage", ge=0)
    sort_by: Optional[GroupSortBy] = Query(default=GroupSortBy.CREATED_AT, alias="sortBy")
    sort_order: Optional[SortOrder] = Query(default=SortOrder.DESC, alias="sortOrder")

    @root_validator
    def validate_date_range(cls, values: dict[str, Any]) -> dict[str, Any]:  # noqa: WPS231, N805
        date_start = values.get("date_start")
        date_end = values.get("date_end")

        if sum(1 for dt in [date_start, date_end] if dt) == 1:
            raise ValueError("Both start date and end date must be provided together")

        if date_start and date_end:
            try:
                start_dt = parser.parse(date_start)
                end_dt = parser.parse(date_end)
            except Exception:
                raise ValueError("Date format used for filtering is invalid")

            if end_dt <= start_dt:
                raise ValueError("End date must be later than start date")

            start_dt = start_dt.replace(hour=0, minute=0, second=0, microsecond=0)
            end_dt = end_dt.replace(hour=23, minute=59, second=59, microsecond=999999)  # noqa: WPS432

            values["date_start"] = start_dt
            values["date_end"] = end_dt

        return values


class GetGroupsResponse(ConfiguredResponseSerializer):
    metadata: GroupsMetadataSerializer = Field(..., alias="meta")
    groups: list[GroupSerializer] = Field(..., alias="result")

    @classmethod
    def from_domain(cls, groups: GroupsInfo) -> "GetGroupsResponse":
        return cls(
            groups=[GroupSerializer.from_domain(group) for group in groups["groups"]],
            metadata=GroupsMetadataSerializer.from_domain(groups["metadata"]),
        )
