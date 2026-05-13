from dataclasses import dataclass

from thelibrary.domain.entities import Review
from thelibrary.domain.repositories import BookRepository, ReviewRepository
from thelibrary.domain.repositories.user_repository import UserRepository
from thelibrary.domain.value_objects import (
    BookId,
    Comment,
    ReviewId,
    ReviewRating,
    UserId,
)
from thelibrary.exceptions.domain_exceptions import (
    InvalidReviewDataError,
    ReviewAlreadyExistsError,
    UserNotFoundError,
)
from thelibrary.use_cases.book import GetBookById, GetBookByIdCommand


@dataclass(frozen=True)
class CreateReviewCommand:
    book_id: str
    rating: int
    comment: str
    user_id: str


class CreateReview:
    def __init__(
        self,
        review_repository: ReviewRepository,
        book_repository: BookRepository,
        user_repository: UserRepository,
    ):
        self.review_repository = review_repository
        self.book_repository = book_repository
        self.user_repository = user_repository

    def execute(self, command: CreateReviewCommand) -> ReviewId:
        try:
            book_id = BookId(command.book_id)
            rating = ReviewRating(command.rating)
            comment = Comment(command.comment)
            user_id = UserId(command.user_id)
        except Exception as e:
            raise InvalidReviewDataError(
                f"Invalid data for review creation: {str(e)}"
            ) from e

        if self.user_repository.get_by_id(user_id) is None:
            raise UserNotFoundError(f"User with ID {user_id.value} was not found")

        existing_review = self.review_repository.get_by_book_id_and_user_id(
            book_id, user_id
        )
        if existing_review is not None:
            raise ReviewAlreadyExistsError(
                f"User with ID {user_id.value} already reviewed book {book_id.value}"
            )

        book = GetBookById(book_repository=self.book_repository).execute(
            GetBookByIdCommand(id=book_id.value)
        )
        review = Review.create(
            id=ReviewId.generate(),
            book_id=book_id,
            rating=rating,
            comment=comment,
            user_id=user_id,
        )

        self.review_repository.save(review)
        book.update_rating(rating)
        book.increment_ratings_count()
        self.book_repository.save(book)
        return review.id
