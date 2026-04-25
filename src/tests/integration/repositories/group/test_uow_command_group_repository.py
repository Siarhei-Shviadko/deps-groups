from uuid import uuid4

import pytest

from deps_groups.domain.model import GroupFactory


def test_group_of_id__success(unit_of_work, group_1, add_document_types, add_groups):
    assert unit_of_work.groups.group_of_id(group_1.id(), group_1.tenant_id()) == group_1


def test_group_of_id__deleted_group_not_found(unit_of_work, group_3, add_document_types, add_groups):
    assert unit_of_work.groups.group_of_id(group_3.id(), group_3.tenant_id()) is None


def test_group_of_id__not_found(unit_of_work):
    assert unit_of_work.groups.group_of_id(uuid4().hex, uuid4().hex) is None


def test_groups_of_ids__success(unit_of_work, group_1, add_document_types, add_groups):
    group_ids = [group_1.id()]
    tenant_id = group_1.tenant_id()
    groups = unit_of_work.groups.groups_of_ids(group_ids, tenant_id)

    assert len(groups) == 1
    assert groups[0] == group_1


def test_groups_of_ids__not_found(unit_of_work):
    group_ids = [uuid4().hex]
    tenant_id = uuid4().hex
    groups = unit_of_work.groups.groups_of_ids(group_ids, tenant_id)

    assert len(groups) == 0


def test_groups_of_ids__deleted_group_not_found(
    unit_of_work, tenant_id, group_1, group_3, add_document_types, add_groups
):
    group_ids = [group_1.id(), group_3.id()]
    groups = unit_of_work.groups.groups_of_ids(group_ids, tenant_id)

    assert len(groups) == 1


def test_save_group__success(unit_of_work, document_type_1, add_document_types):
    test_group = GroupFactory.create(tenant_id=uuid4().hex, name="Test group_1", document_types=[document_type_1.id()])

    unit_of_work.groups.save(test_group)

    saved_group = unit_of_work.groups.group_of_id(test_group.id(), test_group.tenant_id())
    assert saved_group == test_group
    assert saved_group.name == "Test group_1"
    assert [dt() for dt in saved_group.document_types] == [document_type_1.id()]


def test_save_group__update_existing(unit_of_work, group_1, add_document_types, add_groups):
    group_1.name = "Updated group_1 Name"
    unit_of_work.groups.save(group_1)

    updated_group = unit_of_work.groups.group_of_id(group_1.id(), group_1.tenant_id())
    assert updated_group.name == "Updated group_1 Name"


def test_erase_all_groups__success(unit_of_work, group_1, add_document_types, add_groups):
    unit_of_work.groups.erase_all_groups()

    assert unit_of_work.groups.group_of_id(group_1.id(), group_1.tenant_id()) is None
    assert unit_of_work.groups.groups_of_ids([group_1.id()], group_1.tenant_id()) == []


def test_has_group_with_name__success(unit_of_work, group_1, add_document_types, add_groups):
    assert unit_of_work.groups.has_group_with_name(group_1.name, group_1.tenant_id()) is True


def test_has_group_with_name__not_found(unit_of_work):
    assert unit_of_work.groups.has_group_with_name("Nonexistent group_1", uuid4().hex) is False


def test_delete_all__success(unit_of_work, group_3, add_document_types, add_groups):
    unit_of_work.groups.delete_all([group_3])
    assert unit_of_work.groups.group_of_id(group_3.id(), group_3.tenant_id()) is None
