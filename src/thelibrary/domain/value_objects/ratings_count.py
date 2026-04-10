from .base import BaseValueObject


class RatingsCount(BaseValueObject):
    value: int

    def _validate(self) -> None:
        if not isinstance(self.value, int):
            raise TypeError("Book ratings count must be integer")

        if self.value < 0:
            raise ValueError("Book ratings count must be positive integer")
