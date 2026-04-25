from http import HTTPStatus
from uuid import uuid4

from deps_groups.constants import V1_API_PREFIX
from deps_groups.domain.model import GroupSortBy, SortOrder


def test_create_group__group_created(client, document_type_1, document_type_2, add_document_types):
    name = "Test Group"
    document_types = [document_type_1.id(), document_type_2.id()]

    response = client.post(
        f"{V1_API_PREFIX}/groups",
        json={
            "name": name,
            "documentTypeIds": document_types,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["id"] is not None


def test_create_group__existing_name(client, document_type_1, document_type_2, add_document_types, add_groups, group_1):
    name = group_1.name
    document_types = [document_type_1.id(), document_type_2.id()]

    response = client.post(
        f"{V1_API_PREFIX}/groups",
        json={
            "name": name,
            "documentTypeIds": document_types,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT


def test_create_group__missing_name(client, document_type_1):
    document_types = [document_type_1.id()]

    response = client.post(
        f"{V1_API_PREFIX}/groups",
        json={
            "documentTypeIds": document_types,
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_update_group_info__group_updated(client, group_1, add_document_types, add_groups):
    new_name = "Updated Group"

    response = client.patch(
        f"{V1_API_PREFIX}/groups/{group_1.id()}",
        json={
            "name": new_name,
        },
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_update_group_info__optional_tags(client, group_1, add_document_types, add_groups):
    new_name = "Updated Group"

    response = client.patch(
        f"{V1_API_PREFIX}/groups/{group_1.id()}",
        json={
            "name": new_name,
        },
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_groups__groups_deleted(client, group_1, add_document_types, add_groups):
    response = client.delete(
        f"{V1_API_PREFIX}/groups",
        params={"id": [group_1.id()]},
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_add_document_type__document_type_added(client, group_1, document_type_2, add_document_types, add_groups):
    response = client.patch(
        f"{V1_API_PREFIX}/groups/{group_1.id()}/document-types",
        json={
            "documentTypeIds": [document_type_2.id()],
        },
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_remove_document_types__document_types_removed(
    client, group_1, document_type_1, add_document_types, add_groups
):
    response = client.delete(
        f"{V1_API_PREFIX}/groups/{group_1.id()}/document-types",
        params={"id": document_type_1.id()},
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_find_groups(client, test_groups, add_document_types, add_groups, tenant_id):
    name = None
    page = 0
    per_page = 2

    response = client.get(
        f"{V1_API_PREFIX}/groups",
        params={
            "name": name,
            "page": page,
            "perPage": per_page,
            "sortBy": GroupSortBy.CREATED_AT.value,
            "sortOrder": SortOrder.DESC.value,
        },
    )

    assert response.status_code == HTTPStatus.OK

    groups = response.json()

    expected_groups_without_pagination = sorted(
        [group for group in test_groups if not group.is_deleted and group.tenant_id() == tenant_id],
        key=lambda g: g.created_at,
        reverse=True,
    )
    expected_groups = expected_groups_without_pagination[page * per_page : page * per_page + per_page]

    assert len(groups["result"]) == len(expected_groups) == groups["meta"]["size"]

    for group, expected_group in zip(groups["result"], expected_groups):
        assert group["id"] == expected_group.id()

    assert groups["meta"]["total"] == len(expected_groups_without_pagination)


def test_find_group__group_exists(client, group_1, add_document_types, add_groups, tenant_id):
    expected_group = group_1

    response = client.get(f"{V1_API_PREFIX}/groups/{expected_group.id()}")

    assert response.status_code == HTTPStatus.OK

    group = response.json()["group"]

    assert group["id"] == expected_group.id()
    assert group["name"] == expected_group.name
    assert set(group["documentTypeIds"]) == expected_group.document_type_ids


def test_find_group__group_deleted(client, group_3, add_document_types, add_groups, tenant_id):
    expected_group = group_3

    response = client.get(f"{V1_API_PREFIX}/groups/{expected_group.id()}")

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_find_group__group_does_not_exist(client, add_document_types, add_groups, tenant_id):
    response = client.get(f"{V1_API_PREFIX}/groups/{uuid4().hex}")

    assert response.status_code == HTTPStatus.NOT_FOUND
