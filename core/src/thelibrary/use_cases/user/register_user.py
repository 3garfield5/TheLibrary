from dataclasses import dataclass

from thelibrary.domain.entities.user import User
from thelibrary.domain.repositories.user_repository import UserRepository
from thelibrary.domain.value_objects import (
    Email,
    IsAdmin,
    PasswordHash,
    UserId,
    UserName,
)
from thelibrary.exceptions.domain_exceptions import (
    InvalidRegistrationDataError,
    UserAlreadyExistsError,
)


@dataclass(frozen=True)
class RegisterUserCommand:
    username: str
    email: str
    password_hash: str


class RegisterUser:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, command: RegisterUserCommand) -> UserId:
        # Преобразуем в value objects
        try:
            username = UserName(command.username)
            email = Email(command.email)
            password_hash = PasswordHash(command.password_hash)
        except Exception as e:
            raise InvalidRegistrationDataError(
                f"Некорректные данные для регистрации: {str(e)}"
            ) from e

            # Проверяем, существует ли пользователь
        existing_user = self.user_repository.get_by_email(email)
        if existing_user is not None:
            raise UserAlreadyExistsError(
                f"Пользователь с email {email.value} уже существует"
            )

            # Создаем пользователя
        user = User.create(
            id=UserId.generate(),
            username=username,
            email=email,
            password_hash=password_hash,
            is_admin=IsAdmin(
                False
            ),  # по умолчанию обычный пользователь, админов будем создавать вручную в БД или через админку
        )

        # Сохраняем
        self.user_repository.save(user)

        # Возвращаем ID
        return user.id
