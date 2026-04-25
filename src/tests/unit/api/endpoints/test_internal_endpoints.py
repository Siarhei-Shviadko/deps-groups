from http import HTTPStatus

from deps_groups import constants


def test_get_all_groups__empty_repository__returns_empty_list(
    client,
    containers,
    isolated_query_group_service,
):
    with containers.query_group_service.override(isolated_query_group_service):
        response = client.get(f"{constants.INTERNAL_API_PREFIX}/groups")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


def test_get_all_groups__single_group__returns_group(
    client,
    group_1,
    containers,
    isolated_query_group_service,
    isolated_query_group_repository,
):
    isolated_query_group_repository._db = {(group_1.id(), group_1.tenant_id()): group_1}
    with containers.query_group_service.override(isolated_query_group_service):
        response = client.get(f"{constants.INTERNAL_API_PREFIX}/groups")

    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert len(response_data) == 1

    group = response_data[0]
    assert group["id"] == group_1.id()
    assert group["tenant_id"] == group_1.tenant_id()
    assert group["name"] == group_1.name
    assert set(group["document_type_ids"]) == group_1.document_type_ids
    assert group["is_deleted"] == group_1.is_deleted


def test_get_all_groups__multiple_groups__returns_all_groups(
    client,
    group_1,
    group_2,
    containers,
    isolated_query_group_service,
    isolated_query_group_repository,
):
    isolated_query_group_repository._db = {(group.id(), group.tenant_id()): group for group in [group_1, group_2]}
    with containers.query_group_service.override(isolated_query_group_service):
        response = client.get(f"{constants.INTERNAL_API_PREFIX}/groups")

    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert len(response_data) == 2

    group_ids = [g["id"] for g in response_data]
    assert group_1.id() in group_ids
    assert group_2.id() in group_ids


def test_get_all_groups__multi_tenant__returns_groups_from_all_tenants(
    client,
    group_1,
    group_4,
    containers,
    isolated_query_group_service,
    isolated_query_group_repository,
):
    isolated_query_group_repository._db = {(group.id(), group.tenant_id()): group for group in [group_1, group_4]}
    with containers.query_group_service.override(isolated_query_group_service):
        response = client.get(f"{constants.INTERNAL_API_PREFIX}/groups")

    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert len(response_data) == 2

    tenant_ids = [g["tenant_id"] for g in response_data]
    assert group_1.tenant_id() in tenant_ids
    assert group_4.tenant_id() in tenant_ids
    assert group_1.tenant_id() != group_4.tenant_id()


def test_get_all_groups__includes_deleted_groups(
    client,
    group_1,
    group_3,
    containers,
    isolated_query_group_service,
    isolated_query_group_repository,
):
    isolated_query_group_repository._db = {(group.id(), group.tenant_id()): group for group in [group_1, group_3]}
    with containers.query_group_service.override(isolated_query_group_service):
        response = client.get(f"{constants.INTERNAL_API_PREFIX}/groups")

    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert len(response_data) == 2

    deleted_group = next(g for g in response_data if g["id"] == group_3.id())
    assert deleted_group["is_deleted"] is True


def test_internal_api_not_in_openapi(client):
    response = client.get(f"{constants.V1_API_PREFIX}/openapi.json")

    assert response.status_code == HTTPStatus.OK
    response_json = response.json()

    for path in response_json["paths"]:
        assert not path.startswith(constants.INTERNAL_API_PREFIX)
