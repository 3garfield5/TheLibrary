from typing import Optional

from thelibrary.domain.entities import Review
from thelibrary.domain.repositories.review_repository import ReviewRepository
from thelibrary.domain.value_objects import ReviewId, BookId, UserId


class InMemoryReviewRepository(ReviewRepository):
    def __init__(self):
        # храним по id для быстрого доступа
        self._reviews_by_id: dict[ReviewId, Review] = {}

    def save(self, review: Review) -> None:
        self._reviews_by_id[review.id] = review

    def get_by_id(self, id: ReviewId) -> Optional[Review]:
        return self._reviews_by_id.get(id)

    def delete(self, review: Review) -> None:
        self._reviews_by_id.pop(review.id, None)

    def get_by_book_id_and_user_id(
        self, book_id: BookId, user_id: UserId
    ) -> Optional[Review]:
        for review in self._reviews_by_id.values():
            if review.book_id == book_id and review.user_id == user_id:
                return review
        return None
