from __future__ import annotations

from .base import BaseValueObject


class BookId(BaseValueObject):
    value: str

    def _validate(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("Book id must be string")

    @staticmethod
    def generate() -> BookId:
        import uuid

        return BookId(str(uuid.uuid4()))
