from uuid import uuid4

import pytest

from deps_groups.domain.exceptions import DocumentTypesLimitExceeded, IllegalArgument
from deps_groups.domain.model import Group, GroupCreated, GroupFactory, TenantId


def test_create_group_success():
    tenant_id = uuid4().hex
    name = "Test Group"
    document_types = [uuid4().hex for _ in range(3)]

    group = GroupFactory.create(tenant_id, name, document_types)

    assert isinstance(group, Group)
    assert group.tenant_id == TenantId(tenant_id)
    assert group.name == name
    assert len(group.document_types) == 3
    assert len(group.events) == 1
    assert isinstance(group.events[0], GroupCreated)


def test_create_group_with_max_document_types():
    tenant_id = uuid4().hex
    name = "Test Group"
    document_types = [uuid4().hex for _ in range(25)]

    group = GroupFactory.create(tenant_id, name, document_types)

    assert isinstance(group, Group)
    assert group.tenant_id == TenantId(tenant_id)
    assert group.name == name
    assert len(group.document_types) == 25
    assert len(group.events) == 1
    assert isinstance(group.events[0], GroupCreated)


def test_create_group_with_too_much_document_types__fails():
    tenant_id = uuid4().hex
    name = "Test Group"
    document_types = [uuid4().hex for _ in range(26)]
    with pytest.raises(DocumentTypesLimitExceeded):
        GroupFactory.create(tenant_id, name, document_types)


def test_create_group_with_long_name():
    tenant_id = uuid4().hex
    name = "T" * 101
    document_types = [uuid4().hex for _ in range(3)]

    with pytest.raises(IllegalArgument):
        GroupFactory.create(tenant_id, name, document_types)


def test_create_group_with_short_name():
    tenant_id = uuid4().hex
    name = ""
    document_types = [uuid4().hex for _ in range(3)]

    with pytest.raises(IllegalArgument):
        GroupFactory.create(tenant_id, name, document_types)
