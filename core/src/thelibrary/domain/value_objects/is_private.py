from __future__ import annotations

from .base import BaseValueObject


class IsPrivate(BaseValueObject):
    value: bool

    def _validate(self) -> None:
        if not isinstance(self.value, bool):
            raise TypeError("IsPrivate must be a boolean")
