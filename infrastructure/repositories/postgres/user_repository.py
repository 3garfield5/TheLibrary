from __future__ import annotations

from typing import Optional

from sqlalchemy import select

from thelibrary.domain.entities import User
from thelibrary.domain.repositories.user_repository import UserRepository as UserRepositoryContract
from thelibrary.domain.value_objects import Email, IsAdmin, PasswordHash, UserId, UserName

from .database import get_session
from .models import UserModel


class PostgresUserRepository(UserRepositoryContract):
    def save(self, user: User) -> None:
        with get_session() as session:
            db_user = session.get(UserModel, user.id.value)
            if db_user is None:
                db_user = UserModel(id=user.id.value)
                session.add(db_user)

            db_user.username = user.username.value
            db_user.email = user.email.value
            db_user.password_hash = user.password_hash.value
            db_user.is_admin = user.is_admin.value

    def get_by_email(self, email: Email) -> Optional[User]:
        with get_session() as session:
            row = session.scalar(select(UserModel).where(UserModel.email == email.value))

        if row is None:
            return None
        return self._to_entity(row)

    def get_by_id(self, id: UserId) -> Optional[User]:
        with get_session() as session:
            row = session.get(UserModel, id.value)

        if row is None:
            return None
        return self._to_entity(row)

    def delete(self, user: User) -> None:
        with get_session() as session:
            row = session.get(UserModel, user.id.value)
            if row is not None:
                session.delete(row)

    @staticmethod
    def _to_entity(row: UserModel) -> User:
        return User.create(
            id=UserId(row.id),
            username=UserName(row.username),
            email=Email(row.email),
            password_hash=PasswordHash(row.password_hash),
            is_admin=IsAdmin(row.is_admin),
        )
