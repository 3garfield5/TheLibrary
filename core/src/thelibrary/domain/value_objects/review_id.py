from __future__ import annotations

from .base import BaseValueObject


class ReviewId(BaseValueObject):
    value: str

    def _validate(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("Review id must be string")

    @staticmethod
    def generate() -> ReviewId:
        import uuid

        return ReviewId(str(uuid.uuid4()))
