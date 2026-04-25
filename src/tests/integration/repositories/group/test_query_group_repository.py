from deps_groups.domain.model import GroupFiltering, GroupSorting, Pagination, SortOrder


def test_find_all(query_group_repository, group_1, group_2, group_3, test_groups, add_document_types, add_groups):
    groups = query_group_repository.find_all()

    assert len(groups) == len(test_groups)

    for group, expected_group in zip(groups, reversed(test_groups)):
        assert group["id"] == expected_group.id()
        assert group["tenant_id"] == expected_group.tenant_id()
        assert group["name"] == expected_group.name
        assert sorted(group["document_type_ids"]) == sorted([dt() for dt in expected_group.document_types])
        assert group["is_deleted"] == expected_group.is_deleted


def test_find_all_with__zero_parameters(
    query_group_repository,
    test_groups,
    add_document_types,
    add_groups,
):
    groups = query_group_repository.find_all_with()

    assert len(groups["groups"]) == len(test_groups) == groups["metadata"]["total"] == groups["metadata"]["size"]

    for group, expected_group in zip(groups["groups"], sorted(test_groups, key=lambda g: g.created_at, reverse=True)):
        assert group["id"] == expected_group.id()
        assert group["tenant_id"] == expected_group.tenant_id()
        assert group["name"] == expected_group.name
        assert set(group["document_type_ids"]) == expected_group.document_type_ids
        assert group["created_at"] == expected_group.created_at
        assert group["updated_at"] == expected_group.updated_at
        assert group["is_deleted"] == expected_group.is_deleted


def test_find_all_with__custom_sorting(
    query_group_repository,
    test_groups,
    add_document_types,
    add_groups,
):
    groups = query_group_repository.find_all_with(sorting=GroupSorting(sort_order=SortOrder.ASC))

    assert len(groups["groups"]) == len(test_groups) == groups["metadata"]["total"] == groups["metadata"]["size"]

    for group, expected_group in zip(groups["groups"], sorted(test_groups, key=lambda g: g.created_at)):
        assert group["id"] == expected_group.id()


def test_find_all_with__filtering(
    query_group_repository,
    test_groups_of_tenant_1,
    tenant_id,
    group_1,
    test_groups,
    add_document_types,
    add_groups,
):
    groups = query_group_repository.find_all_with(filtering=GroupFiltering(tenant_id=tenant_id))

    assert (
        len(groups["groups"])
        == len(test_groups_of_tenant_1)
        == groups["metadata"]["total"]
        == groups["metadata"]["size"]
    )

    for group, expected_group in zip(
        groups["groups"], sorted(test_groups_of_tenant_1, key=lambda g: g.created_at, reverse=True)
    ):
        assert group["id"] == expected_group.id()
        assert group["tenant_id"] == expected_group.tenant_id()

    groups = query_group_repository.find_all_with(filtering=GroupFiltering(tenant_id=tenant_id, name=group_1.name))

    assert len(groups["groups"]) == 1
    assert groups["groups"][0]["id"] == group_1.id()

    groups = query_group_repository.find_all_with(filtering=GroupFiltering(is_deleted=False))

    not_deleted_groups = sorted(
        [group for group in test_groups if not group.is_deleted], key=lambda g: g.created_at, reverse=True
    )

    assert len(groups["groups"]) == len(not_deleted_groups)

    for group, expected_group in zip(groups["groups"], not_deleted_groups):
        assert group["id"] == expected_group.id()


def test_find_all_with__pagination(
    query_group_repository,
    test_groups,
    add_document_types,
    add_groups,
):
    page = 1
    per_page = 2

    expected_groups = sorted(test_groups, key=lambda g: g.created_at, reverse=True)[
        page * per_page : page * per_page + per_page
    ]

    groups = query_group_repository.find_all_with(pagination=Pagination(page=page, per_page=per_page))

    assert len(groups["groups"]) == len(expected_groups)  # == groups["metadata"]["size"]
    assert len(test_groups) == groups["metadata"]["total"]

    for group, expected_group in zip(groups["groups"], expected_groups):
        assert group["id"] == expected_group.id()


def test_find__group_exists(
    query_group_repository,
    group_1,
    add_document_types,
    add_groups,
    tenant_id,
):
    expected_group = group_1

    group = query_group_repository.find(group_id=expected_group.id(), tenant_id=tenant_id)

    assert group
    assert group["id"] == expected_group.id()
    assert group["name"] == expected_group.name
    assert set(group["document_type_ids"]) == expected_group.document_type_ids


def test_find__group_deleted(
    query_group_repository,
    group_3,
    add_document_types,
    add_groups,
    tenant_id,
):
    expected_group = group_3

    assert not query_group_repository.find(group_id=expected_group.id(), tenant_id=tenant_id)
