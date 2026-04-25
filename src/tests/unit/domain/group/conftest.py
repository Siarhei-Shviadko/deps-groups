from uuid import uuid4

import pytest

from deps_groups.domain.model import GroupFactory


@pytest.fixture
def name():
    return uuid4().hex


@pytest.fixture
def document_types():
    return [uuid4().hex for _ in range(24)]


@pytest.fixture
def group(tenant_id, name, document_types):
    group = GroupFactory.create(
        tenant_id=tenant_id,
        name=name,
        document_types=document_types,
    )

    group.events.clear()

    return group
