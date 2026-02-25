from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class BaseValueObject:
    value: object

    def __post_init__(self):
        self._validate()
    
    def _validate(self):
        pass

    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.value})'
