from abc import ABC, abstractmethod
from typing import Optional

from thelibrary.domain.entities import User
from thelibrary.domain.value_objects import Email, UserId


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        pass

    @abstractmethod
    def get_by_email(self, email: Email) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_id(self, id: UserId) -> Optional[User]:
        pass

    @abstractmethod
    def delete(self, user: User) -> None:
        pass
