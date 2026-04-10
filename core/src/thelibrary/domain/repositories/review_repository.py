from abc import ABC, abstractmethod
from typing import Optional

from thelibrary.domain.entities import Review
from thelibrary.domain.value_objects import BookId, ReviewId, UserId


class ReviewRepository(ABC):
    @abstractmethod
    def save(self, review: Review) -> None:
        pass

    @abstractmethod
    def get_by_id(self, id: ReviewId) -> Optional[Review]:
        pass

    @abstractmethod
    def delete(self, review: Review) -> None:
        pass

    @abstractmethod
    def get_by_book_id_and_user_id(
        self, book_id: BookId, user_id: UserId
    ) -> Optional[Review]:
        pass
