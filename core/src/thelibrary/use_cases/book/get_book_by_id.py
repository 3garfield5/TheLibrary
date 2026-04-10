from dataclasses import dataclass

from thelibrary.domain.entities import Book
from thelibrary.domain.repositories.book_repository import BookRepository
from thelibrary.domain.value_objects import BookId
from thelibrary.exceptions.domain_exceptions import (
    BookNotFoundError,
    InvalidBookDataError,
)


@dataclass(frozen=True)
class GetBookByIdCommand:
    id: str


class GetBookById:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    def execute(self, command: GetBookByIdCommand) -> Book:
        # Преобразуем в value objects
        try:
            id = BookId(command.id)
        except Exception as e:
            raise InvalidBookDataError(
                f"Некорректные данные для получения книги: {str(e)}"
            ) from e

        # Проверяем, существует ли книга
        book = self.book_repository.get_by_id(id)
        if book is None:
            raise BookNotFoundError(f"Книга с ID {id.value} не найдена")

        return book
