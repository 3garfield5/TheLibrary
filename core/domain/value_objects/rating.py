from .base import BaseValueObject

class Rating(BaseValueObject):
    value: float

    def _validate(self):
        if not isinstance(self.value, float):
            raise TypeError("Book rating must be float")
        
        if not (1 <= self.value <= 10):
            raise ValueError("Book rating must be between 1 and 10")