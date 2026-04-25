from uuid import uuid4

import pytest

from deps_groups.domain.exceptions import DocumentTypeNotFound, IllegalArgument


def test_save_all__success(document_type_service):
    dt_id_1, dt_id_2, tenant_id = uuid4().hex, uuid4().hex, uuid4().hex

    document_types_info = [
        {"document_type_id": dt_id_1, "tenant_id": tenant_id},
        {"document_type_id": dt_id_2, "tenant_id": tenant_id},
    ]

    document_types = document_type_service.save_all(document_types_info)

    assert len(document_types) == 2

    document_type_1, document_type_2 = document_types

    assert document_type_1.id() == dt_id_1
    assert document_type_1.tenant_id() == tenant_id

    assert document_type_2.id() == dt_id_2
    assert document_type_2.tenant_id() == tenant_id


def test_save_all__empty_list(document_type_service):
    document_types_info = []

    document_types = document_type_service.save_all(document_types_info)

    assert len(document_types) == 0


def test_save_all__invalid_data(document_type_service):
    dt_id_1, tenant_id = uuid4().hex, uuid4().hex

    document_types_info = [
        {"document_type_id": dt_id_1, "tenant_id": tenant_id},
        {"document_type_id": None, "tenant_id": tenant_id},
    ]

    with pytest.raises(IllegalArgument):
        document_type_service.save_all(document_types_info)


def test_create__success(document_type_service):
    dt_id, tenant_id = uuid4().hex, uuid4().hex

    document_type = document_type_service.create(dt_id, tenant_id)

    assert document_type.id() == dt_id
    assert document_type.tenant_id() == tenant_id


def test_create__missing_id(document_type_service):
    tenant_id = uuid4().hex

    with pytest.raises(IllegalArgument):
        document_type_service.create(None, tenant_id)


def test_create__missing_tenant_id(document_type_service):
    dt_id = uuid4().hex

    with pytest.raises(IllegalArgument):
        document_type_service.create(dt_id, None)


def test_create__invalid_id_type(document_type_service):
    tenant_id = uuid4().hex

    with pytest.raises(IllegalArgument):
        document_type_service.create(123, tenant_id)


def test_create__invalid_tenant_id_type(document_type_service):
    dt_id = uuid4().hex

    with pytest.raises(IllegalArgument):
        document_type_service.create(dt_id, 456)


def test_delete__success(document_type_service, document_type_1, tenant_id, add_document_types):
    document_type = document_type_service.delete(document_type_1.id(), tenant_id)

    assert document_type.id() == document_type_1.id()
    assert document_type.tenant_id() == tenant_id


def test_delete__nonexistent_document_type(document_type_service):
    dt_id, tenant_id = uuid4().hex, uuid4().hex

    with pytest.raises(DocumentTypeNotFound):
        document_type_service.delete(dt_id, tenant_id)
