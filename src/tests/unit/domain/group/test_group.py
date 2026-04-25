from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from deps_groups.domain.exceptions import IllegalArgument, LimitExceededError
from deps_groups.domain.model import (
    DocumentTypesAdded,
    DocumentTypesRemoved,
    EntityId,
    GroupDeleted,
    GroupInfoUpdated,
)


def test_update_info(group):
    new_name = "Updated Group"
    group.update_info(new_name)

    assert group.name == new_name
    assert group.updated_at > datetime.now() - timedelta(seconds=1)
    assert len(group.events) == 1
    assert isinstance(group.events[0], GroupInfoUpdated)


def test_delete_group(group):
    group.delete()

    assert group.updated_at > datetime.now() - timedelta(seconds=1)
    assert len(group.events) == 1
    assert isinstance(group.events[0], GroupDeleted)


def test_add_document_type(group):
    document_type_id = uuid4().hex
    group.add_document_types([document_type_id])

    assert EntityId(document_type_id) in group.document_types
    assert group.updated_at > datetime.now() - timedelta(seconds=1)
    assert len(group.events) == 1
    assert isinstance(group.events[0], DocumentTypesAdded)


def test_remove_document_type(group, document_types):
    document_type_id = document_types[0]

    group.remove_document_types([document_type_id])

    assert EntityId(document_type_id) not in group.document_types
    assert group.updated_at > datetime.now() - timedelta(seconds=1)
    assert len(group.events) == 1
    assert isinstance(group.events[0], DocumentTypesRemoved)


def test_update_info_with_long_name(group):
    new_name = "T" * 101

    with pytest.raises(IllegalArgument):
        group.update_info(new_name)


def test_add_document_type_with_too_many_document_types(group):
    new_document_type_id_1 = uuid4().hex
    new_document_type_id_2 = uuid4().hex

    group.add_document_types([new_document_type_id_1])

    with pytest.raises(LimitExceededError):
        group.add_document_types([new_document_type_id_2])


def test_add_existing_document_type(group):
    group.document_types.clear()

    document_type_id = uuid4().hex

    group.add_document_types([document_type_id])
    group.add_document_types([document_type_id])

    assert len(group.document_types) == 1
    assert len(group.events) == 1


def test_remove_nonexistent_document_type(group, document_types):
    document_type_id = uuid4().hex
    group.remove_document_types([document_type_id])

    assert len(group.document_types) == len(document_types)
    assert len(group.events) == 0  # No event should be added


def test_deletion(group):
    assert not group.is_deleted

    group.delete()

    assert group.is_deleted
