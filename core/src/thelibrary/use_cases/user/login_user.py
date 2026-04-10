from dataclasses import dataclass

from thelibrary.domain.repositories.user_repository import UserRepository
from thelibrary.domain.value_objects import Email, PasswordHash, UserId
from thelibrary.exceptions.domain_exceptions import (
    InvalidLoginDataError,
    UserNotFoundError,
)


@dataclass(frozen=True)
class LoginUserCommand:
    email: str
    password_hash: str


class LoginUser:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, command: LoginUserCommand) -> UserId:
        # Преобразуем в value objects
        try:
            email = Email(command.email)
            password_hash = PasswordHash(command.password_hash)
        except Exception as e:
            raise InvalidLoginDataError(
                f"Некорректные данные для входа: {str(e)}"
            ) from e

        # Проверяем, существует ли пользователь
        user = self.user_repository.get_by_email(email)
        if user is None:
            raise UserNotFoundError(f"Пользователь с email {email.value} не найден")

        # Проверяем пароль
        if user.password_hash != password_hash:
            raise InvalidLoginDataError("Неверный пароль")

        return user.id
