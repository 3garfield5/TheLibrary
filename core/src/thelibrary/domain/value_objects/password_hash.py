from __future__ import annotations

from .base import BaseValueObject


class PasswordHash(BaseValueObject):
    value: str

    def _validate(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("Password hash must be string")

        if len(self.value) == 0:
            raise ValueError("Password hash cannot be empty")

        object.__setattr__(self, "value", self.value)
