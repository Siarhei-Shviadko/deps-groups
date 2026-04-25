from dataclasses import dataclass

__all__ = ["Pagination"]


@dataclass
class Pagination:
    per_page: int
    page: int

    @property
    def offset(self) -> int:
        return self.per_page * self.page

    @property
    def first_element_index(self) -> int:
        return self.offset

    @property
    def last_element_index(self) -> int:
        return self.first_element_index + self.per_page
