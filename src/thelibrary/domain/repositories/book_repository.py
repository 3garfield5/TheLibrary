from abc import ABC, abstractmethod
from typing import Optional

from thelibrary.domain.entities import Book
from thelibrary.domain.value_objects import BookId, Title


class BookRepository(ABC):
    @abstractmethod
    def save(self, book: Book) -> None:
        pass

    @abstractmethod
    def get_by_id(self, id: BookId) -> Optional[Book]:
        pass

    @abstractmethod
    def get_by_title(self, title: Title) -> Optional[Book]:
        pass

    @abstractmethod
    def delete(self, book: Book) -> None:
        pass
