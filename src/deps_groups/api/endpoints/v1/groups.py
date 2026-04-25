from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, status

from deps_groups.application import CommandGroupService, QueryGroupService
from deps_groups.containers import Containers

from ...auth import get_current_user_tenant
from ...endpoint_marker import MarkerRoute
from ...endpoint_visibility import Visibility
from ...serializers import (
    AddDocumentTypesRequest,
    CreateGroupRequest,
    CreateGroupResponse,
    GetGroupResponse,
    GetGroupsRequest,
    GetGroupsResponse,
    UpdateGroupInfoRequest,
)

__all__ = ["groups_router"]


groups_router = APIRouter(prefix="/groups", tags=["Groups"], route_class=MarkerRoute)


@groups_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    openapi_extra={"visibility": Visibility.INTERNAL},
    response_model=CreateGroupResponse,
)
@inject
def create_group(
    create_group_request: CreateGroupRequest,
    current_tenant: str = Depends(get_current_user_tenant),
    command_group_service: CommandGroupService = Depends(Provide[Containers.command_group_service]),
):
    return CreateGroupResponse.from_domain(
        command_group_service.create(
            tenant_id=current_tenant,
            name=create_group_request.name,
            document_type_ids=create_group_request.document_type_ids,
        ),
    )


@groups_router.patch(
    "/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    openapi_extra={"visibility": Visibility.INTERNAL},
)
@inject
def update_group_info(
    group_id: str,
    update_group_info_request: UpdateGroupInfoRequest,
    current_tenant: str = Depends(get_current_user_tenant),
    command_group_service: CommandGroupService = Depends(Provide[Containers.command_group_service]),
):
    command_group_service.update_info(
        id_=group_id,
        tenant_id=current_tenant,
        name=update_group_info_request.name,
    )


@groups_router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
    openapi_extra={"visibility": Visibility.INTERNAL},
)
@inject
def delete_groups(
    ids: list[str] = Query(..., alias="id"),
    current_tenant: str = Depends(get_current_user_tenant),
    command_group_service: CommandGroupService = Depends(Provide[Containers.command_group_service]),
):
    command_group_service.delete(ids=ids, tenant_id=current_tenant)


@groups_router.patch(
    "/{group_id}/document-types",
    status_code=status.HTTP_204_NO_CONTENT,
    openapi_extra={"visibility": Visibility.INTERNAL},
)
@inject
def add_document_types(
    group_id: str,
    add_document_request: AddDocumentTypesRequest,
    current_tenant: str = Depends(get_current_user_tenant),
    command_group_service: CommandGroupService = Depends(Provide[Containers.command_group_service]),
):
    command_group_service.add_document_types(
        id_=group_id,
        tenant_id=current_tenant,
        document_types_ids=add_document_request.document_types_ids,
    )


@groups_router.delete(
    "/{group_id}/document-types",
    status_code=status.HTTP_204_NO_CONTENT,
    openapi_extra={"visibility": Visibility.INTERNAL},
)
@inject
def remove_document_types(
    group_id: str,
    ids: list[str] = Query(..., alias="id"),
    current_tenant: str = Depends(get_current_user_tenant),
    command_group_service: CommandGroupService = Depends(Provide[Containers.command_group_service]),
):
    command_group_service.remove_document_types(
        id_=group_id,
        tenant_id=current_tenant,
        document_types_ids=ids,
    )


@groups_router.get(
    "",
    status_code=status.HTTP_200_OK,
    openapi_extra={"visibility": Visibility.INTERNAL},
    response_model=GetGroupsResponse,
)
@inject
def get_groups(
    tenant_id: str = Depends(get_current_user_tenant),
    get_groups_request: GetGroupsRequest = Depends(),
    query_group_service: QueryGroupService = Depends(Provide[Containers.query_group_service]),
):
    return GetGroupsResponse.from_domain(
        query_group_service.find_all_with(
            tenant_id=tenant_id,
            name=get_groups_request.name,
            is_deleted=False,
            document_type_id=get_groups_request.document_type_id,
            datetime_range=(
                (
                    get_groups_request.date_start,
                    get_groups_request.date_end,
                )
                if get_groups_request.date_start and get_groups_request.date_end
                else None
            ),
            page=get_groups_request.page,
            per_page=get_groups_request.per_page,
            sort_by=get_groups_request.sort_by,
            sort_order=get_groups_request.sort_order,
        ),
    )


@groups_router.get(
    "/{group_id}",
    status_code=status.HTTP_200_OK,
    openapi_extra={"visibility": Visibility.INTERNAL},
    response_model=GetGroupResponse,
)
@inject
def get_group(
    group_id: str,
    tenant_id: str = Depends(get_current_user_tenant),
    query_group_service: QueryGroupService = Depends(Provide[Containers.query_group_service]),
):
    return GetGroupResponse.from_domain(
        query_group_service.find(
            group_id=group_id,
            tenant_id=tenant_id,
        ),
    )
