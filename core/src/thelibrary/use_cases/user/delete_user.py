from dataclasses import dataclass

from thelibrary.domain.repositories.user_repository import UserRepository
from thelibrary.domain.value_objects import UserId
from thelibrary.exceptions.domain_exceptions import (
    InvalidUserDataError,
    UserNotFoundError,
)


@dataclass(frozen=True)
class DeleteUserCommand:
    id: str


class DeleteUser:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, command: DeleteUserCommand) -> None:
        # Преобразуем в value objects
        try:
            user_id = UserId(command.id)
        except Exception as e:
            raise InvalidUserDataError(
                f"Некорректные данные для удаления пользователя: {str(e)}"
            ) from e

        # Проверяем, существует ли пользователь
        user = self.user_repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"Пользователь с ID {user_id.value} не найден")

        self.user_repository.delete(user)
