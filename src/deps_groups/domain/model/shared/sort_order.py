from .extended_enum import ExtendedEnum

__all__ = ["SortOrder"]


class SortOrder(ExtendedEnum):
    ASC = "asc"
    DESC = "desc"
