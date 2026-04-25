import pytest


@pytest.fixture
def unit_of_work(containers):
    return containers.unit_of_work()


@pytest.fixture(autouse=True)
def empty_unit_of_work(unit_of_work):
    try:
        with unit_of_work:
            unit_of_work.document_types.erase_all_document_types()
            unit_of_work.groups.erase_all_groups()
            unit_of_work.commit()

        yield

        with unit_of_work:
            unit_of_work.document_types.erase_all_document_types()
            unit_of_work.groups.erase_all_groups()
            unit_of_work.commit()
    except Exception as e:
        pass


@pytest.fixture
def query_group_repository(repositories):
    return repositories.query_group()


@pytest.fixture()
def add_document_types(unit_of_work, test_document_types):
    with unit_of_work:
        for document_type in test_document_types:
            unit_of_work.document_types.save_new(document_type)

        unit_of_work.commit()

        yield


@pytest.fixture()
def add_groups(unit_of_work, test_groups):
    with unit_of_work:
        for group in test_groups:
            unit_of_work.groups.save(group)

        unit_of_work.commit()

        yield
