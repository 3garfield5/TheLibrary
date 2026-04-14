from typing import Optional

from thelibrary.domain.entities import Book
from thelibrary.domain.repositories.book_repository import BookRepository
from thelibrary.domain.value_objects import BookId


class InMemoryBookRepository(BookRepository):
    def __init__(self):
        # храним по id для быстрого доступа
        self._books_by_id: dict[BookId, Book] = {}

    def save(self, book: Book) -> None:
        self._books_by_id[book.id] = book

    def get_by_id(self, id: BookId) -> Optional[Book]:
        return self._books_by_id.get(id)

    def get_by_title(self, title: str) -> Optional[Book]:
        for book in self._books_by_id.values():
            if book.title == title:
                return book
        return None

    def delete(self, book: Book) -> None:
        self._books_by_id.pop(book.id, None)
