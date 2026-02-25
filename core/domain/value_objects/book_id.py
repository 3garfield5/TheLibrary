from .base import BaseValueObject

class BookId(BaseValueObject):
    value: int

    def _validate(self):
        if not isinstance(self.value, int):
            raise TypeError("Book id must be integer")
        
        if self.value < 1:
            raise ValueError("Book id must be positive integer")
