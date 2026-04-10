from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BaseValueObject:
    value: object

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        pass

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"
