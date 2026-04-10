from __future__ import annotations

from .base import BaseValueObject


class Email(BaseValueObject):
    value: str

    def _validate(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("Email must be string")

        value = self.value.strip()

        if "@" not in value or value.startswith("@") or value.endswith("@"):
            raise ValueError("Invalid email format")

        object.__setattr__(self, "value", value)
