from __future__ import annotations

from .base import BaseValueObject


class IsAdmin(BaseValueObject):
    value: bool

    def _validate(self) -> None:
        if not isinstance(self.value, bool):
            raise TypeError("IsAdmin must be a boolean")
