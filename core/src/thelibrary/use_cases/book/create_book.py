from dataclasses import dataclass

from thelibrary.domain.entities import Book
from thelibrary.domain.repositories.book_repository import BookRepository
from thelibrary.domain.repositories.user_repository import UserRepository
from thelibrary.domain.value_objects import (
    Author,
    BookId,
    Rating,
    RatingsCount,
    ReleaseYear,
    Title,
    UserId,
)
from thelibrary.exceptions.domain_exceptions import (
    BookAlreadyExistsError,
    InvalidBookDataError,
    PermissionDeniedError,
    UserNotFoundError,
)


@dataclass(frozen=True)
class CreateBookCommand:
    title: str
    author: str
    release_year: int
    admin_user_id: str


class CreateBook:
    def __init__(self, book_repository: BookRepository, user_repository: UserRepository):
        self.book_repository = book_repository
        self.user_repository = user_repository

    def execute(self, command: CreateBookCommand) -> BookId:
        try:
            title = Title(command.title)
            author = Author(command.author)
            release_year = ReleaseYear(command.release_year)
            admin_user_id = UserId(command.admin_user_id)
        except Exception as e:
            raise InvalidBookDataError(f"Invalid data for book creation: {str(e)}") from e

        admin = self.user_repository.get_by_id(admin_user_id)
        if admin is None:
            raise UserNotFoundError(f"User with ID {admin_user_id.value} was not found")
        if not admin.is_admin.value:
            raise PermissionDeniedError("Only admin users can create books")

        existing_book = self.book_repository.get_by_title(title)
        if existing_book is not None:
            raise BookAlreadyExistsError(
                f"Book with title {title.value} already exists"
            )

        book = Book.create(
            id=BookId.generate(),
            title=title,
            author=author,
            rating=Rating(0.0),
            ratings_count=RatingsCount(0),
            release_year=release_year,
        )

        self.book_repository.save(book)
        return book.id
