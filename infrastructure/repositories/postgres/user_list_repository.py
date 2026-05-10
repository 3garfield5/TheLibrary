from __future__ import annotations

from typing import Optional

from sqlalchemy import delete, select

from thelibrary.domain.entities import UserList
from thelibrary.domain.repositories.user_list_repository import (
    UserListRepository as UserListRepositoryContract,
)
from thelibrary.domain.value_objects import (
    BookId,
    Description,
    IsPrivate,
    UserId,
    UserListId,
    UserListTitle,
)

from .database import get_session
from .models import UserListBookModel, UserListModel


class PostgresUserListRepository(UserListRepositoryContract):
    def save(self, user_list: UserList) -> None:
        with get_session() as session:
            db_user_list = session.get(UserListModel, user_list.id.value)
            if db_user_list is None:
                db_user_list = UserListModel(id=user_list.id.value)
                session.add(db_user_list)

            db_user_list.title = user_list.title.value
            db_user_list.description = user_list.description.value
            db_user_list.is_private = user_list.is_private.value
            db_user_list.user_id = user_list.user_id.value

            session.execute(
                delete(UserListBookModel).where(
                    UserListBookModel.user_list_id == user_list.id.value
                )
            )
            for book_id in user_list.books:
                session.add(
                    UserListBookModel(
                        user_list_id=user_list.id.value,
                        book_id=book_id.value,
                    )
                )

    def get_by_id(self, id: UserListId) -> Optional[UserList]:
        with get_session() as session:
            row = session.get(UserListModel, id.value)
            if row is None:
                return None
            book_ids = self._get_book_ids(session, row.id)

        return self._to_entity(row, book_ids)

    def delete(self, user_list: UserList) -> None:
        with get_session() as session:
            row = session.get(UserListModel, user_list.id.value)
            if row is not None:
                session.delete(row)

    def get_by_user_id(self, user_id: UserId) -> list[UserList]:
        with get_session() as session:
            rows = list(
                session.scalars(
                    select(UserListModel).where(UserListModel.user_id == user_id.value)
                )
            )
            books_by_list_id = {
                row.id: self._get_book_ids(session, row.id) for row in rows
            }

        return [self._to_entity(row, books_by_list_id[row.id]) for row in rows]

    @staticmethod
    def _get_book_ids(session, user_list_id: str) -> list[BookId]:
        values = session.scalars(
            select(UserListBookModel.book_id).where(
                UserListBookModel.user_list_id == user_list_id
            )
        )
        return [BookId(value) for value in values]

    @staticmethod
    def _to_entity(row: UserListModel, books: list[BookId]) -> UserList:
        return UserList.create(
            id=UserListId(row.id),
            title=UserListTitle(row.title),
            description=Description(row.description),
            user_id=UserId(row.user_id),
            is_private=IsPrivate(row.is_private),
            books=books,
        )
