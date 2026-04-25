__all__ = ["GroupsException", "NotFoundError", "IllegalArgument", "AlreadyExistsError", "LimitExceededError"]


class GroupsException(Exception):
    code = "groups_exception"


class BusinessException(GroupsException):
    code = "business_exception"


class NotFoundError(GroupsException):
    code = "not_found_error"


class AlreadyExistsError(GroupsException):
    code = "already_created_error"


class IllegalArgument(GroupsException):
    code = "illegal_argument"


class LimitExceededError(GroupsException):
    code = "limit_exceeded_error"
