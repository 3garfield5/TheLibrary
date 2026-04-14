from __future__ import annotations

from .base import BaseValueObject


class Rating(BaseValueObject):
    value: float

    def _validate(self) -> None:
        if not isinstance(self.value, float):
            raise TypeError("Book rating must be float")

        if not (0 <= self.value <= 10):
            raise ValueError("Book rating must be between 0 and 10")
