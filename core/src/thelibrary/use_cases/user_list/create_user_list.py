from dataclasses import dataclass

from thelibrary.domain.entities import UserList
from thelibrary.domain.repositories.user_repository import UserRepository
from thelibrary.domain.repositories.user_list_repository import UserListRepository
from thelibrary.domain.value_objects import (
    Description,
    IsPrivate,
    UserId,
    UserListId,
    UserListTitle,
)
from thelibrary.exceptions.domain_exceptions import (
    InvalidUserListDataError,
    UserListAlreadyExistsError,
    UserNotFoundError,
)


@dataclass(frozen=True)
class CreateUserListCommand:
    title: str
    description: str
    is_private: bool
    user_id: str


class CreateUserList:
    def __init__(
        self,
        user_list_repository: UserListRepository,
        user_repository: UserRepository,
    ):
        self.user_list_repository = user_list_repository
        self.user_repository = user_repository

    def execute(self, command: CreateUserListCommand) -> UserListId:
        try:
            title = UserListTitle(command.title)
            description = Description(command.description)
            is_private = IsPrivate(command.is_private)
            user_id = UserId(command.user_id)
        except Exception as e:
            raise InvalidUserListDataError(
                f"Invalid data for user list creation: {str(e)}"
            ) from e

        if self.user_repository.get_by_id(user_id) is None:
            raise UserNotFoundError(f"User with ID {user_id.value} was not found")

        existing_user_lists = self.user_list_repository.get_by_user_id(user_id)
        for user_list in existing_user_lists:
            if user_list.title.value == title.value:
                raise UserListAlreadyExistsError(
                    f"User list with title {title.value} already exists"
                )

        user_list = UserList.create(
            id=UserListId.generate(),
            title=title,
            description=description,
            user_id=user_id,
            is_private=is_private,
        )

        self.user_list_repository.save(user_list)
        return user_list.id
