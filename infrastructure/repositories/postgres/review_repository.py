from __future__ import annotations

from typing import Optional

from sqlalchemy import select

from thelibrary.domain.entities import Review
from thelibrary.domain.repositories.review_repository import (
    ReviewRepository as ReviewRepositoryContract,
)
from thelibrary.domain.value_objects import BookId, Comment, ReviewId, ReviewRating, UserId

from .database import get_session
from .models import ReviewModel


class PostgresReviewRepository(ReviewRepositoryContract):
    def save(self, review: Review) -> None:
        with get_session() as session:
            db_review = session.get(ReviewModel, review.id.value)
            if db_review is None:
                db_review = ReviewModel(id=review.id.value)
                session.add(db_review)

            db_review.rating = review.rating.value
            db_review.comment = review.comment.value
            db_review.book_id = review.book_id.value
            db_review.user_id = review.user_id.value

    def get_by_id(self, id: ReviewId) -> Optional[Review]:
        with get_session() as session:
            row = session.get(ReviewModel, id.value)

        if row is None:
            return None
        return self._to_entity(row)

    def delete(self, review: Review) -> None:
        with get_session() as session:
            row = session.get(ReviewModel, review.id.value)
            if row is not None:
                session.delete(row)

    def get_by_book_id_and_user_id(
        self, book_id: BookId, user_id: UserId
    ) -> Optional[Review]:
        with get_session() as session:
            row = session.scalar(
                select(ReviewModel).where(
                    ReviewModel.book_id == book_id.value,
                    ReviewModel.user_id == user_id.value,
                )
            )

        if row is None:
            return None
        return self._to_entity(row)

    @staticmethod
    def _to_entity(row: ReviewModel) -> Review:
        return Review.create(
            id=ReviewId(row.id),
            rating=ReviewRating(row.rating),
            comment=Comment(row.comment),
            book_id=BookId(row.book_id),
            user_id=UserId(row.user_id),
        )
