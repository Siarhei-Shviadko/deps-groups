import pytest

from deps_groups.application import QueryGroupService
from tests.fakes.query_group_repository import FakeQueryGroupRepository


@pytest.fixture
def isolated_query_group_repository():
    return FakeQueryGroupRepository()


@pytest.fixture
def isolated_query_group_service(isolated_query_group_repository):
    return QueryGroupService(
        query_group_repository=isolated_query_group_repository,
        default_page=0,
        default_per_page=10,
    )
