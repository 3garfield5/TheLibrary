from dataclasses import dataclass

from thelibrary.domain.repositories.book_repository import BookRepository
from thelibrary.domain.repositories.user_list_repository import UserListRepository
from thelibrary.domain.value_objects import BookId, UserListId
from thelibrary.exceptions.domain_exceptions import (
    BookAlreadyInUserListError,
    BookNotFoundError,
    InvalidUserListDataError,
    UserListNotFoundError,
)


@dataclass(frozen=True)
class AddBookToUserListCommand:
    user_list_id: str
    book_id: str


class AddBookToUserList:
    def __init__(
        self,
        user_list_repository: UserListRepository,
        book_repository: BookRepository,
    ):
        self.user_list_repository = user_list_repository
        self.book_repository = book_repository

    def execute(self, command: AddBookToUserListCommand) -> None:
        try:
            user_list_id = UserListId(command.user_list_id)
            book_id = BookId(command.book_id)
        except Exception as e:
            raise InvalidUserListDataError(
                f"Invalid data for adding book to user list: {str(e)}"
            ) from e

        user_list = self.user_list_repository.get_by_id(user_list_id)
        if user_list is None:
            raise UserListNotFoundError(
                f"User list with ID {user_list_id.value} was not found"
            )

        if self.book_repository.get_by_id(book_id) is None:
            raise BookNotFoundError(f"Book with ID {book_id.value} was not found")

        if user_list.has_book(book_id):
            raise BookAlreadyInUserListError(
                f"Book with ID {book_id.value} is already in user list"
            )

        user_list.add_book(book_id)
        self.user_list_repository.save(user_list)
