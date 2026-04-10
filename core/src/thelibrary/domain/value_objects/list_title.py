from __future__ import annotations

from .base import BaseValueObject


class UserListTitle(BaseValueObject):
    value: str

    def _validate(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("UserList title must be string")

        value = self.value.strip()

        if len(value) < 2:
            raise ValueError("UserList title must be at least 2 characters")

        object.__setattr__(self, "value", value)
