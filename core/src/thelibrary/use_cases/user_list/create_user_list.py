from dataclasses import dataclass

from thelibrary.domain.entities import UserList
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
)


@dataclass(frozen=True)
class CreateUserListCommand:
    title: str
    description: str
    is_private: bool
    user_id: str


class CreateUserList:
    def __init__(self, user_list_repository: UserListRepository):
        self.user_list_repository = user_list_repository

    def execute(self, command: CreateUserListCommand) -> UserListId:
        # Преобразуем в value objects
        try:
            title = UserListTitle(command.title)
            description = Description(command.description)
            is_private = IsPrivate(command.is_private)
            user_id = UserId(command.user_id)
        except Exception as e:
            raise InvalidUserListDataError(
                f"Некорректные данные для создания списка: {str(e)}"
            ) from e

        # Проверяем, существует ли список у пользователя с таким же названием
        existing_user_lists = self.user_list_repository.get_by_user_id(user_id.value)
        for user_list in existing_user_lists or []:
            if user_list.title.value == title.value:
                raise UserListAlreadyExistsError(
                    f"Список с названием {title.value} уже существует"
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
