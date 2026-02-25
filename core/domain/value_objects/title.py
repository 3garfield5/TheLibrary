from .base import BaseValueObject

class Title(BaseValueObject):
    value: str

    def _validate(self):
        if not isinstance(self.value, str):
            raise TypeError("Book title must be string")
        
        value = self.value.strip()
        
        if len(value) < 2:
            raise ValueError("Book title must be at least 2 characters")
        
        object.__setattr__(self, "value", value)