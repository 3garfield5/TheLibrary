from dataclasses import dataclass

from thelibrary.domain.entities import UserList
from thelibrary.domain.repositories.user_list_repository import UserListRepository
from thelibrary.domain.value_objects import UserListId
from thelibrary.exceptions.domain_exceptions import (
    InvalidUserListDataError,
    UserListNotFoundError,
)


@dataclass(frozen=True)
class GetUserListByIdCommand:
    id: str


class GetUserListById:
    def __init__(self, user_list_repository: UserListRepository):
        self.user_list_repository = user_list_repository

    def execute(self, command: GetUserListByIdCommand) -> UserList:
        try:
            id = UserListId(command.id)
        except Exception as e:
            raise InvalidUserListDataError(f"Invalid user list id: {str(e)}") from e

        user_list = self.user_list_repository.get_by_id(id)
        if user_list is None:
            raise UserListNotFoundError(f"User list with ID {id.value} was not found")

        return user_list
