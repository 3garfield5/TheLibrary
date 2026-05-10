from dataclasses import dataclass

from thelibrary.domain.entities import Book
from thelibrary.domain.repositories.book_repository import BookRepository
from thelibrary.domain.repositories.user_repository import UserRepository
from thelibrary.domain.value_objects import Author, BookId, ReleaseYear, Title, UserId
from thelibrary.exceptions.domain_exceptions import (
    BookAlreadyExistsError,
    BookNotFoundError,
    InvalidBookDataError,
    PermissionDeniedError,
    UserNotFoundError,
)


@dataclass(frozen=True)
class UpdateBookCommand:
    id: str
    title: str
    author: str
    release_year: int
    admin_user_id: str


class UpdateBook:
    def __init__(self, book_repository: BookRepository, user_repository: UserRepository):
        self.book_repository = book_repository
        self.user_repository = user_repository

    def execute(self, command: UpdateBookCommand) -> Book:
        try:
            id = BookId(command.id)
            title = Title(command.title)
            author = Author(command.author)
            release_year = ReleaseYear(command.release_year)
            admin_user_id = UserId(command.admin_user_id)
        except Exception as e:
            raise InvalidBookDataError(f"Invalid data for book update: {str(e)}") from e

        admin = self.user_repository.get_by_id(admin_user_id)
        if admin is None:
            raise UserNotFoundError(f"User with ID {admin_user_id.value} was not found")
        if not admin.is_admin.value:
            raise PermissionDeniedError("Only admin users can update books")

        book = self.book_repository.get_by_id(id)
        if book is None:
            raise BookNotFoundError(f"Book with ID {id.value} was not found")

        existing_book = self.book_repository.get_by_title(title)
        if existing_book is not None and existing_book.id != book.id:
            raise BookAlreadyExistsError(
                f"Book with title {title.value} already exists"
            )

        book.update_details(title=title, author=author, release_year=release_year)
        self.book_repository.save(book)
        return book
