from __future__ import annotations

from .base import BaseValueObject


class Description(BaseValueObject):
    value: str

    def _validate(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("Description must be string")

        value = self.value.strip()

        object.__setattr__(self, "value", value)
