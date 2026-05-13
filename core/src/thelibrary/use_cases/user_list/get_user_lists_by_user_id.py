from dataclasses import dataclass

from thelibrary.domain.entities import UserList
from thelibrary.domain.repositories.user_repository import UserRepository
from thelibrary.domain.repositories.user_list_repository import UserListRepository
from thelibrary.domain.value_objects import UserId
from thelibrary.exceptions.domain_exceptions import (
    InvalidUserListDataError,
    UserNotFoundError,
)


@dataclass(frozen=True)
class GetUserListsByUserIdCommand:
    user_id: str


class GetUserListsByUserId:
    def __init__(
        self,
        user_list_repository: UserListRepository,
        user_repository: UserRepository,
    ):
        self.user_list_repository = user_list_repository
        self.user_repository = user_repository

    def execute(self, command: GetUserListsByUserIdCommand) -> list[UserList]:
        try:
            user_id = UserId(command.user_id)
        except Exception as e:
            raise InvalidUserListDataError(
                f"Invalid user id for user lists lookup: {str(e)}"
            ) from e

        if self.user_repository.get_by_id(user_id) is None:
            raise UserNotFoundError(f"User with ID {user_id.value} was not found")

        return self.user_list_repository.get_by_user_id(user_id)
