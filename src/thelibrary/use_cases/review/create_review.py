from dataclasses import dataclass

from thelibrary.domain.entities import Review
from thelibrary.domain.repositories.review_repository import ReviewRepository
from thelibrary.domain.value_objects import BookId, Comment, Rating, ReviewId, UserId
from thelibrary.exceptions.domain_exceptions import (
    InvalidReviewDataError,
    ReviewAlreadyExistsError,
)


@dataclass(frozen=True)
class CreateReviewCommand:
    book_id: str
    rating: float
    comment: str
    user_id: str


class CreateReview:
    def __init__(self, review_repository: ReviewRepository):
        self.review_repository = review_repository

    def execute(self, command: CreateReviewCommand) -> ReviewId:
        # Преобразуем в value objects
        try:
            book_id = BookId(command.book_id)
            rating = Rating(command.rating)
            comment = Comment(command.comment)
            user_id = UserId(command.user_id)
        except Exception as e:
            raise InvalidReviewDataError(
                f"Некорректные данные для создания отзыва: {str(e)}"
            ) from e
        
        # Проверяем, есть ли уже отзыв от этого пользователя на эту книгу
        existing_review = self.review_repository.get_by_book_id_and_user_id(book_id, user_id)
        if existing_review is not None:
            raise ReviewAlreadyExistsError(
                f"Пользователь с ID {user_id.value} уже оставил отзыв на книгу с ID {book_id.value}"
            )

        review = Review.create(
            id=ReviewId.generate(),
            book_id=book_id,
            rating=rating,
            comment=comment,
            user_id=user_id
        )

        self.review_repository.save(review)
        return review.id