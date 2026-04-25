from datetime import datetime

import pytest

from deps_groups.domain.exceptions import GroupNotFound
from deps_groups.domain.model import GroupSortBy, SortOrder


def test_find_all(query_group_service, test_groups, add_document_types, add_groups):
    groups = query_group_service.find_all()

    assert len(groups) == len(test_groups)

    for group, expected_group in zip(groups, reversed(test_groups)):
        assert group["id"] == expected_group.id()
        assert group["tenant_id"] == expected_group.tenant_id()
        assert group["name"] == expected_group.name
        assert set(group["document_type_ids"]) == expected_group.document_type_ids


def test_find_all_with(query_group_service, test_groups, add_document_types, add_groups, tenant_id):
    page = 0
    per_page = 2
    is_deleted = False

    groups = query_group_service.find_all_with(
        tenant_id=tenant_id,
        is_deleted=is_deleted,
        page=page,
        per_page=per_page,
        sort_order=SortOrder.ASC,
        sort_by=GroupSortBy.CREATED_AT,
    )

    expected_groups_without_pagination = sorted(
        [group for group in test_groups if not group.is_deleted and group.tenant_id() == tenant_id],
        key=lambda g: g.created_at,
    )
    expected_groups = expected_groups_without_pagination[page * per_page : page * per_page + per_page]

    assert len(groups["groups"]) == len(expected_groups) == groups["metadata"]["size"]

    for group, expected_group in zip(groups["groups"], expected_groups):
        assert group["id"] == expected_group.id()

    assert groups["metadata"]["total"] == len(expected_groups_without_pagination)


def test_find_with_name(query_group_service, test_groups, add_document_types, add_groups, tenant_id):
    page = 0
    per_page = 10
    is_deleted = False
    name = test_groups[0].name

    groups = query_group_service.find_all_with(
        tenant_id=tenant_id,
        is_deleted=is_deleted,
        name=name,
        page=page,
        per_page=per_page,
        sort_order=SortOrder.ASC,
        sort_by=GroupSortBy.CREATED_AT,
    )

    expected_groups_without_pagination = sorted(
        [
            group
            for group in test_groups
            if not group.is_deleted and group.tenant_id() == tenant_id and group.name == name
        ],
        key=lambda g: g.created_at,
    )
    expected_groups = expected_groups_without_pagination[page * per_page : page * per_page + per_page]

    assert len(groups["groups"]) == len(expected_groups) == groups["metadata"]["size"]

    for group, expected_group in zip(groups["groups"], expected_groups):
        assert group["id"] == expected_group.id()

    assert groups["metadata"]["total"] == len(expected_groups_without_pagination)


def test_find_with_document_type(
    query_group_service, document_type_1, test_groups, add_document_types, add_groups, tenant_id
):
    page = 0
    per_page = 10
    is_deleted = False
    document_type_id = document_type_1.id()

    groups = query_group_service.find_all_with(
        tenant_id=tenant_id,
        is_deleted=is_deleted,
        document_type_id=document_type_id,
        page=page,
        per_page=per_page,
        sort_order=SortOrder.ASC,
        sort_by=GroupSortBy.CREATED_AT,
    )

    expected_groups_without_pagination = sorted(
        [
            group
            for group in test_groups
            if not group.is_deleted
            and group.tenant_id() == tenant_id
            and document_type_id in [type_() for type_ in group.document_types]
        ],
        key=lambda g: g.created_at,
    )
    expected_groups = expected_groups_without_pagination[page * per_page : page * per_page + per_page]

    assert len(groups["groups"]) == len(expected_groups) == groups["metadata"]["size"]

    for group, expected_group in zip(groups["groups"], expected_groups):
        assert group["id"] == expected_group.id()

    assert groups["metadata"]["total"] == len(expected_groups_without_pagination)


def test_find_with_datetime_range(query_group_service, test_groups, add_document_types, add_groups, tenant_id):
    page = 0
    per_page = 10
    is_deleted = False
    datetime_start, datetime_end = datetime(year=2000, month=1, day=1), datetime(year=2001, month=1, day=1)

    groups = query_group_service.find_all_with(
        tenant_id=tenant_id,
        is_deleted=is_deleted,
        datetime_range=(
            datetime_start,
            datetime_end,
        ),
        page=page,
        per_page=per_page,
        sort_order=SortOrder.ASC,
        sort_by=GroupSortBy.CREATED_AT,
    )

    assert len(groups["groups"]) == 0 == groups["metadata"]["size"]
    assert groups["metadata"]["total"] == 0


def test_find__group_exists(
    query_group_service,
    group_1,
    add_document_types,
    add_groups,
    tenant_id,
):
    expected_group = group_1

    group = query_group_service.find(group_id=expected_group.id(), tenant_id=tenant_id)

    assert group
    assert group["id"] == expected_group.id()
    assert group["name"] == expected_group.name
    assert set(group["document_type_ids"]) == expected_group.document_type_ids


def test_find__group_deleted(
    query_group_service,
    group_3,
    add_document_types,
    add_groups,
    tenant_id,
):
    expected_group = group_3

    with pytest.raises(GroupNotFound):
        query_group_service.find(group_id=expected_group.id(), tenant_id=tenant_id)
