from uuid import uuid4

import pytest

from deps_groups.domain.exceptions import (
    DocumentTypesNotFound,
    GroupNotFound,
    GroupWithNameAlreadyExists,
)


def test_create__success(command_group_service, tenant_id, document_type_1, add_document_types):
    name = uuid4().hex
    document_type_ids = [document_type_1.id()]

    group = command_group_service.create(tenant_id, name, document_type_ids)

    assert group.name == name
    assert [dt() for dt in group.document_types] == document_type_ids


def test_create__group_with_name_already_exists(
    command_group_service, tenant_id, document_type_1, group_1, add_document_types, add_groups
):
    document_type_ids = [document_type_1.id()]

    with pytest.raises(GroupWithNameAlreadyExists):
        command_group_service.create(tenant_id, group_1.name, document_type_ids)


def test_create__invalid_document_types(command_group_service, tenant_id):
    name = uuid4().hex
    document_type_ids = [uuid4().hex for _ in range(3)]

    with pytest.raises(DocumentTypesNotFound):
        command_group_service.create(tenant_id, name, document_type_ids)


def test_update_info__success(command_group_service, tenant_id, group_1, add_document_types, add_groups):
    new_name = uuid4().hex

    updated_group = command_group_service.update_info(group_1.id(), tenant_id, new_name)

    assert updated_group.name == new_name


def test_update_info__same_info(command_group_service, tenant_id, group_1, add_document_types, add_groups):
    new_name = group_1.name

    updated_group = command_group_service.update_info(group_1.id(), tenant_id, new_name)

    assert updated_group.name == new_name


def test_update_info__group_not_found(command_group_service, tenant_id):
    with pytest.raises(GroupNotFound):
        command_group_service.update_info(uuid4().hex, tenant_id, uuid4().hex)


def test_delete__success(command_group_service, tenant_id, group_1, add_document_types, add_groups):
    deleted_groups = command_group_service.delete([group_1.id()], tenant_id)

    assert len(deleted_groups) == 1
    assert deleted_groups[0].id() == group_1.id()
    assert deleted_groups[0].is_deleted


def test_delete__multiple_groups(command_group_service, tenant_id, group_1, add_document_types, add_groups):
    group_ids = [group_1.id()]
    deleted_groups = command_group_service.delete(group_ids, tenant_id)

    assert len(deleted_groups) == len(group_ids)
    assert sorted([group.id() for group in deleted_groups]) == sorted(group_ids)
    assert all([group.is_deleted for group in deleted_groups])


def test_add_document_type__success(
    command_group_service, tenant_id, group_1, document_type_2, add_document_types, add_groups
):
    group = command_group_service.add_document_types(group_1.id(), tenant_id, [document_type_2.id()])

    assert document_type_2.id() in [dt() for dt in group.document_types]


def test_add_document_type__invalid_document_types(
    command_group_service, tenant_id, group_1, add_document_types, add_groups
):
    document_type_ids = [uuid4().hex for _ in range(3)]

    with pytest.raises(DocumentTypesNotFound):
        command_group_service.add_document_types(group_1.id(), tenant_id, document_type_ids)


def test_add_document_type__group_not_found(command_group_service, tenant_id, document_type_2, add_document_types):
    with pytest.raises(GroupNotFound):
        command_group_service.add_document_types(uuid4().hex, tenant_id, [document_type_2.id()])


def test_remove_document_type__success(
    command_group_service, tenant_id, group_1, document_type_1, add_document_types, add_groups
):
    group = command_group_service.remove_document_types(group_1.id(), tenant_id, [document_type_1.id()])

    assert document_type_1.id() not in [dt() for dt in group.document_types]


def test_remove_document_type__group_not_found(command_group_service, tenant_id, document_type_1):
    with pytest.raises(GroupNotFound):
        command_group_service.remove_document_types(uuid4().hex, tenant_id, [document_type_1.id()])
