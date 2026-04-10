from .base import BaseValueObject


class Rating(BaseValueObject):
    value: int

    def _validate(self) -> None:
        if not isinstance(self.value, int):
            raise TypeError("Review rating must be int")

        if not (1 <= self.value <= 10):
            raise ValueError("Review rating must be between 1 and 10")
