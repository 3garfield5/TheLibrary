from abc import ABC, abstractmethod
from typing import Optional

from thelibrary.domain.entities import UserList
from thelibrary.domain.value_objects import UserListId


class UserListRepository(ABC):
    @abstractmethod
    def save(self, user_list: UserList) -> None:
        pass

    @abstractmethod
    def get_by_id(self, id: UserListId) -> Optional[UserList]:
        pass

    @abstractmethod
    def delete(self, user_list: UserList) -> None:
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: str) -> Optional[list[UserList]]:
        pass
