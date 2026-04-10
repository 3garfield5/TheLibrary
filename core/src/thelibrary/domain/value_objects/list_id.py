from __future__ import annotations

from .base import BaseValueObject


class UserListId(BaseValueObject):
    value: str

    def _validate(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("UserList id must be string")

    @staticmethod
    def generate() -> UserListId:
        import uuid

        return UserListId(str(uuid.uuid4()))
