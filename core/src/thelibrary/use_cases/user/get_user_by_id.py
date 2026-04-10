from dataclasses import dataclass

from thelibrary.domain.entities import User
from thelibrary.domain.repositories.user_repository import UserRepository
from thelibrary.domain.value_objects import UserId
from thelibrary.exceptions.domain_exceptions import (
    UserNotFoundError,
    InvalidUserDataError,
)


@dataclass(frozen=True)
class GetUserByIdCommand:
    id: str


class GetUserById:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, command: GetUserByIdCommand) -> User:
        # Преобразуем в value objects
        try:
            id = UserId(command.id)
        except Exception as e:
            raise InvalidUserDataError(
                f"Некорректные данные для получения пользователя: {str(e)}"
            ) from e

        # Проверяем, существует ли пользователь
        user = self.user_repository.get_by_id(id)
        if user is None:
            raise UserNotFoundError(f"Пользователь с ID {id.value} не найден")

        return user