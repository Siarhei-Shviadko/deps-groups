from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from deps_groups.application import QueryGroupService
from deps_groups.containers import Containers

__all__ = ["internal_router"]

internal_router = APIRouter(prefix="/groups")


@internal_router.get(
    "",
    status_code=status.HTTP_200_OK,
)
@inject
def get_all_groups(
    service: QueryGroupService = Depends(Provide[Containers.query_group_service]),
) -> list:
    return service.find_all()
