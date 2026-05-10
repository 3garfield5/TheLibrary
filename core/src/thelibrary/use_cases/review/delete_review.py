from dataclasses import dataclass

from thelibrary.domain.repositories import BookRepository, ReviewRepository
from thelibrary.domain.repositories.user_repository import UserRepository
from thelibrary.domain.value_objects import ReviewId, UserId
from thelibrary.exceptions.domain_exceptions import (
    InvalidReviewDataError,
    PermissionDeniedError,
    ReviewNotFoundError,
    UserNotFoundError,
)
from thelibrary.use_cases.book import GetBookById, GetBookByIdCommand


@dataclass(frozen=True)
class DeleteReviewCommand:
    id: str
    user_id: str


class DeleteReview:
    def __init__(
        self,
        review_repository: ReviewRepository,
        book_repository: BookRepository,
        user_repository: UserRepository,
    ):
        self.review_repository = review_repository
        self.book_repository = book_repository
        self.user_repository = user_repository

    def execute(self, command: DeleteReviewCommand) -> None:
        try:
            id = ReviewId(command.id)
            user_id = UserId(command.user_id)
        except Exception as e:
            raise InvalidReviewDataError(
                f"Invalid data for review delete: {str(e)}"
            ) from e

        user = self.user_repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"User with ID {user_id.value} was not found")

        review = self.review_repository.get_by_id(id)
        if review is None:
            raise ReviewNotFoundError(f"Review with ID {id.value} was not found")

        if review.user_id != user.id and not user.is_admin.value:
            raise PermissionDeniedError("Users can delete only their own reviews")

        self.review_repository.delete(review)
        book = GetBookById(book_repository=self.book_repository).execute(
            GetBookByIdCommand(id=review.book_id.value)
        )
        book.remove_rating(review.rating)
        self.book_repository.save(book)
