from .base import AlreadyExistsError, LimitExceededError, NotFoundError

__all__ = ["GroupWithNameAlreadyExists", "DocumentTypesNotFound", "GroupNotFound", "DocumentTypesLimitExceeded"]


class GroupWithNameAlreadyExists(AlreadyExistsError):
    code = "group_with_name_already_exists"

    def __init__(self, name: str) -> None:
        super().__init__(f"Group with name `{name}` already exists.")


class DocumentTypesNotFound(NotFoundError):
    code = "document_types_not_found"

    def __init__(self, document_types_ids: str) -> None:
        super().__init__(f"Document Types `{document_types_ids}` are not found.")


class GroupNotFound(NotFoundError):
    code = "group_not_found"

    def __init__(self, group_id: str, tenant_id: str) -> None:
        super().__init__(f"Group `{group_id}` in tenant `{tenant_id}` is not found.")


class DocumentTypesLimitExceeded(LimitExceededError):
    code = "document_types_limit_exceeded"

    def __init__(self, max_limit: int) -> None:
        super().__init__(f"The maximum number of document types that can be added to the group is {max_limit}.")
