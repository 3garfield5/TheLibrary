from .base import BaseValueObject


class UserId(BaseValueObject):
    value: str

    def _validate(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("User id must be string")
        
    @staticmethod
    def generate() -> UserId:
        import uuid
        return UserId(str(uuid.uuid4()))
