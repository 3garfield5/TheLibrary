from .base import BaseValueObject


class Comment(BaseValueObject):
    value: str

    def _validate(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("Review comment must be string")

        value = self.value.strip()

        object.__setattr__(self, "value", value)
