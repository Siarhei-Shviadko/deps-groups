import abc

from deps_groups.domain.model import ICommandGroupRepository, IDocumentTypeRepository

__all__ = ["AbstractUnitOfWork"]


class AbstractUnitOfWork(abc.ABC):
    document_types: IDocumentTypeRepository
    groups: ICommandGroupRepository

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError
