from uuid import uuid4

from deps_groups.domain.model import DocumentTypeFactory


def test_get_document_type__success(unit_of_work, document_type_1, add_document_types):
    assert (
        unit_of_work.document_types.document_type_of_id(document_type_1.id(), document_type_1.tenant_id())
        == document_type_1
    )


def test_get_document_type__not_found(unit_of_work, document_type_1, add_document_types):
    assert unit_of_work.document_types.document_type_of_id(document_type_1.id(), uuid4().hex) is None


def test_save_document_type__success(unit_of_work):
    test_document_type = DocumentTypeFactory.create(id_=uuid4().hex, tenant_id=uuid4().hex)

    unit_of_work.document_types.save_new(test_document_type)

    assert (
        unit_of_work.document_types.document_type_of_id(test_document_type.id(), test_document_type.tenant_id())
        == test_document_type
    )


def test_save_document_type__dt_already_saved(unit_of_work, document_type_1, add_document_types):
    unit_of_work.document_types.save_new(document_type_1)

    assert (
        unit_of_work.document_types.document_type_of_id(document_type_1.id(), document_type_1.tenant_id())
        == document_type_1
    )


def test_save_all__success(unit_of_work):
    document_types = [DocumentTypeFactory.create(id_=uuid4().hex, tenant_id=uuid4().hex) for _ in range(3)]

    for document_type in document_types:
        assert unit_of_work.document_types.document_type_of_id(document_type.id(), document_type.tenant_id()) is None

    unit_of_work.document_types.save_all(document_types)

    for document_type in document_types:
        assert (
            unit_of_work.document_types.document_type_of_id(document_type.id(), document_type.tenant_id())
            == document_type
        )


def test_save_all__already_added(unit_of_work, document_type_1, add_document_types):
    document_types = [DocumentTypeFactory.create(id_=uuid4().hex, tenant_id=uuid4().hex) for _ in range(3)]

    for document_type_1 in document_types:
        assert (
            unit_of_work.document_types.document_type_of_id(document_type_1.id(), document_type_1.tenant_id()) is None
        )

    document_types.append(document_type_1)

    unit_of_work.document_types.save_all(document_types)

    for document_type_1 in document_types:
        assert (
            unit_of_work.document_types.document_type_of_id(document_type_1.id(), document_type_1.tenant_id())
            == document_type_1
        )


def test_delete_document_type__success(unit_of_work, document_type_1, add_document_types):
    assert (
        unit_of_work.document_types.document_type_of_id(document_type_1.id(), document_type_1.tenant_id())
        == document_type_1
    )

    unit_of_work.document_types.delete(document_type_1)

    assert unit_of_work.document_types.document_type_of_id(document_type_1.id(), document_type_1.tenant_id()) is None


def test_delete_document_type__not_found(unit_of_work):
    test_document_type = DocumentTypeFactory.create(id_=uuid4().hex, tenant_id=uuid4().hex)

    unit_of_work.document_types.delete(test_document_type)


def test_document_types_of_invalid_ids__all_valid(unit_of_work, document_type_1, add_document_types):
    document_type_ids = [document_type_1.id()]

    result = unit_of_work.document_types.document_types_of_invalid_ids(document_type_ids, document_type_1.tenant_id())

    assert result == []


def test_document_types_of_invalid_ids__none_valid(unit_of_work):
    document_type_ids = [uuid4().hex for _ in range(3)]

    result = unit_of_work.document_types.document_types_of_invalid_ids(document_type_ids, uuid4().hex)

    assert sorted(result) == sorted(document_type_ids)


def test_document_types_of_invalid_ids__some_valid(unit_of_work, document_type_1, add_document_types):
    document_type_ids = [document_type_1.id(), uuid4().hex, uuid4().hex]

    result = unit_of_work.document_types.document_types_of_invalid_ids(document_type_ids, document_type_1.tenant_id())
    expected_result = document_type_ids[1:]

    assert sorted(result) == sorted(expected_result)
