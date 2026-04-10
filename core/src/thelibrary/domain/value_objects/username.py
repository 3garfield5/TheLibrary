from .base import BaseValueObject


class UserName(BaseValueObject):
    value: str

    def _validate(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("User name must be string")

        value = self.value.strip()

        if len(value) < 2:
            raise ValueError("User name must be at least 2 characters")

        object.__setattr__(self, "value", value)
