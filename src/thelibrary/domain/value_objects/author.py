from .base import BaseValueObject


class Author(BaseValueObject):
    value: str

    def _validate(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("Book author must be string")

        value = self.value.strip()

        if len(value) < 2:
            raise ValueError("Book author must be at least 2 characters")

        object.__setattr__(self, "value", value)
