import pytest

from tests.fakes.query_group_repository import FakeQueryGroupRepository


@pytest.fixture
def postgres_session_mock(mocker, containers):
    mock = mocker.Mock(containers.datasources.postgres_session())
    containers.datasources.postgres_session.override(mock)

    yield mock

    containers.datasources.postgres_session.reset_override()


@pytest.fixture
def fake_query_group_repository(repositories):
    with repositories.query_group.override(FakeQueryGroupRepository()):
        yield repositories.query_group()

    repositories.query_group.reset_override()
