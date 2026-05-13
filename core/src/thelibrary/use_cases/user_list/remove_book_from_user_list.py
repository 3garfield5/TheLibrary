from dataclasses import dataclass

from thelibrary.domain.repositories.user_list_repository import UserListRepository
from thelibrary.domain.value_objects import BookId, UserListId
from thelibrary.exceptions.domain_exceptions import (
    BookNotInUserListError,
    InvalidUserListDataError,
    UserListNotFoundError,
)


@dataclass(frozen=True)
class RemoveBookFromUserListCommand:
    user_list_id: str
    book_id: str


class RemoveBookFromUserList:
    def __init__(self, user_list_repository: UserListRepository):
        self.user_list_repository = user_list_repository

    def execute(self, command: RemoveBookFromUserListCommand) -> None:
        try:
            user_list_id = UserListId(command.user_list_id)
            book_id = BookId(command.book_id)
        except Exception as e:
            raise InvalidUserListDataError(
                f"Invalid data for removing book from user list: {str(e)}"
            ) from e

        user_list = self.user_list_repository.get_by_id(user_list_id)
        if user_list is None:
            raise UserListNotFoundError(
                f"User list with ID {user_list_id.value} was not found"
            )

        if not user_list.has_book(book_id):
            raise BookNotInUserListError(
                f"Book with ID {book_id.value} is not in user list"
            )

        user_list.remove_book(book_id)
        self.user_list_repository.save(user_list)
