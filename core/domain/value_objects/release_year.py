from .base import BaseValueObject
from datetime import datetime

class ReleaseYear(BaseValueObject):
    value: int

    def _validate(self):
        if not isinstance(self.value, int):
            raise TypeError("Book release year must be integer")
        
        current_year = datetime.now().year
        
        if not (1 <= self.value <= current_year):
            raise ValueError("Invalid release year")