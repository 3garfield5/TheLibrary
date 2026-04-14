from typing import Optional

from thelibrary.domain.entities import User
from thelibrary.domain.repositories.user_repository import UserRepository
from thelibrary.domain.value_objects import Email, UserId


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        # храним по id для быстрого доступа
        self._users_by_id: dict[UserId, User] = {}
        self._users_by_email: dict[Email, User] = {}

    def save(self, user: User) -> None:
        # если пользователь уже есть — обновляем
        existing = self._users_by_id.get(user.id)

        if existing:
            # если email изменился — обновляем индекс
            if existing.email != user.email:
                self._users_by_email.pop(existing.email, None)

        self._users_by_id[user.id] = user
        self._users_by_email[user.email] = user

    def get_by_email(self, email: Email) -> Optional[User]:
        return self._users_by_email.get(email)

    def get_by_id(self, id: UserId) -> Optional[User]:
        return self._users_by_id.get(id)

    def delete(self, user: User) -> None:
        self._users_by_id.pop(user.id, None)
        self._users_by_email.pop(user.email, None)
