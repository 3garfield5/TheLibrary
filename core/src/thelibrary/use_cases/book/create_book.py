from dataclasses import dataclass

from thelibrary.domain.entities import Book
from thelibrary.domain.repositories.book_repository import BookRepository
from thelibrary.domain.value_objects import (
    Author,
    BookId,
    Rating,
    RatingsCount,
    ReleaseYear,
    Title,
)
from thelibrary.exceptions.domain_exceptions import (
    BookAlreadyExistsError,
    InvalidBookDataError,
)


@dataclass(frozen=True)
class CreateBookCommand:
    title: str
    author: str
    rating: float
    ratings_count: int
    release_year: int


class CreateBook:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    def execute(self, command: CreateBookCommand) -> BookId:
        # Преобразуем в value objects
        try:
            title = Title(command.title)
            author = Author(command.author)
            rating = Rating(command.rating)
            ratings_count = RatingsCount(command.ratings_count)
            release_year = ReleaseYear(command.release_year)
        except Exception as e:
            raise InvalidBookDataError(
                f"Некорректные данные для создания книги: {str(e)}"
            ) from e

        # Проверяем, существует ли книга
        existing_book = self.book_repository.get_by_title(title)
        if existing_book is not None:
            raise BookAlreadyExistsError(
                f"Книга с названием {title.value} уже существует"
            )

        book = Book.create(
            id=BookId.generate(),
            title=title,
            author=author,
            rating=rating,
            ratings_count=ratings_count,
            release_year=release_year,
        )

        self.book_repository.save(book)
        return book.id
