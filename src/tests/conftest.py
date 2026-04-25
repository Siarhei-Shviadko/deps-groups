from unittest.mock import Mock
from uuid import uuid4

import pytest
from starlette.testclient import TestClient

from deps_groups import api
from deps_groups.domain.model import DocumentTypeFactory, GroupFactory
from deps_groups.entrypoint import create_fastapi
from deps_groups.infrastructure.access_management import user


@pytest.fixture(scope="session")
def app():
    fastapi_app = create_fastapi()
    yield fastapi_app


@pytest.fixture
def client(app):
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def containers(app):
    return app.containers


@pytest.fixture(autouse=True, scope="session")
def domain_event_publisher_session_mock(containers):
    mock = Mock(containers.domain_event_publisher())
    containers.domain_event_publisher.override(mock)

    yield mock

    containers.domain_event_publisher.reset_override()


@pytest.fixture(autouse=True)
def domain_event_publisher_mock(domain_event_publisher_session_mock):
    domain_event_publisher_session_mock.reset_mock()

    yield domain_event_publisher_session_mock


@pytest.fixture
def repositories(containers):
    return containers.repositories


@pytest.fixture
def query_user_service(containers):
    return containers.query_user_service()


@pytest.fixture
def query_group_service(containers):
    return containers.query_group_service()


@pytest.fixture
def command_group_service(containers):
    return containers.command_group_service()


@pytest.fixture
def document_type_service(containers):
    return containers.document_type_service()


@pytest.fixture
def tenant_id():
    return uuid4().hex


@pytest.fixture
def tenant_id_2():
    return uuid4().hex


@pytest.fixture
def document_type_1(tenant_id):
    return DocumentTypeFactory.create(id_=uuid4().hex, tenant_id=tenant_id)


@pytest.fixture
def document_type_2(tenant_id):
    return DocumentTypeFactory.create(id_=uuid4().hex, tenant_id=tenant_id)


@pytest.fixture
def document_type_3(tenant_id_2):
    return DocumentTypeFactory.create(id_=uuid4().hex, tenant_id=tenant_id_2)


@pytest.fixture
def group_1(tenant_id, document_type_1):
    group = GroupFactory.create(
        tenant_id=tenant_id,
        name=uuid4().hex,
        document_types=[document_type_1.id()],
    )

    group.events.clear()

    return group


@pytest.fixture
def group_2(tenant_id, document_type_1, document_type_2):
    group = GroupFactory.create(
        tenant_id=tenant_id,
        name=uuid4().hex,
        document_types=[document_type_1.id(), document_type_2.id()],
    )

    group.events.clear()

    return group


@pytest.fixture
def group_3(tenant_id, document_type_1):
    group = GroupFactory.create(
        tenant_id=tenant_id,
        name=uuid4().hex,
        document_types=[document_type_1.id()],
    )
    group.delete()
    group.events.clear()

    return group


@pytest.fixture
def group_4(tenant_id_2, document_type_3):
    group = GroupFactory.create(
        tenant_id=tenant_id_2,
        name=uuid4().hex,
        document_types=[document_type_3.id()],
    )
    group.events.clear()

    return group


@pytest.fixture
def group_5(tenant_id_2):
    group = GroupFactory.create(
        tenant_id=tenant_id_2,
        name=uuid4().hex,
        document_types=[],
    )
    group.events.clear()

    return group


@pytest.fixture
def test_document_types(document_type_1, document_type_2, document_type_3):
    return [document_type_1, document_type_2, document_type_3]


@pytest.fixture
def test_groups(group_1, group_2, group_3, group_4, group_5):
    return [group_1, group_2, group_3, group_4, group_5]


@pytest.fixture
def test_groups_of_tenant_1(group_1, group_2, group_3):
    return [group_1, group_2, group_3]


@pytest.fixture
def test_groups_of_tenant_2(group_4, group_5):
    return [group_4, group_5]


@pytest.fixture
def this_user(tenant_id):
    return dict(
        subject="Test",
        groups=[tenant_id],
        token="token",
        roles=[],
        organisation=tenant_id,
    )


@pytest.fixture(autouse=True)
def set_this_user(this_user):
    user.set(this_user)


@pytest.fixture(autouse=True)
def mocked_middleware(monkeypatch, mocker):
    monkeypatch.setattr(api.auth, "set_user_from_token", mocker.Mock({}))
