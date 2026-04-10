from __future__ import annotations

from thelibrary.domain.value_objects import (
    BookId,
    Description,
    IsPrivate,
    UserId,
    UserListId,
    UserListTitle,
)


class UserList:
    def __init__(
        self,
        id: UserListId,
        title: UserListTitle,
        description: Description,
        user_id: UserId,
        is_private: IsPrivate,
        books: list[BookId] | None = None,
    ):
        self._id: UserListId = id
        self._title: UserListTitle = title
        self._description: Description = description
        self._is_private: IsPrivate = is_private
        self._user_id: UserId = user_id
        self._books: list[BookId] = books if books is not None else []

    @property
    def id(self) -> UserListId:
        return self._id

    @property
    def title(self) -> UserListTitle:
        return self._title

    @property
    def is_private(self) -> IsPrivate:
        return self._is_private

    @property
    def description(self) -> Description:
        return self._description

    @property
    def user_id(self) -> UserId:
        return self._user_id

    @property
    def books(self) -> list[BookId]:
        return self._books

    def __str__(self) -> str:
        return f'Список с названием "{self.title.value}" и {len(self.books)} книгами'

    @classmethod
    def create(
        cls,
        id: UserListId,
        title: UserListTitle,
        description: Description,
        user_id: UserId,
        is_private: IsPrivate,
        books: list[BookId] | None = None,
    ) -> UserList:
        return cls(
            id=id, title=title, description=description, user_id=user_id, is_private=is_private, books=books
        )

    # fill with methods
