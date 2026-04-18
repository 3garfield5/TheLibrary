from dataclasses import dataclass

from thelibrary.domain.repositories import ReviewRepository, BookRepository
from thelibrary.domain.value_objects import ReviewId
from thelibrary.exceptions.domain_exceptions import (
    InvalidReviewDataError,
    ReviewNotFoundError,
)
from thelibrary.use_cases.book import GetBookById, GetBookByIdCommand


@dataclass(frozen=True)
class DeleteReviewCommand:
    id: str


class DeleteReview:
    def __init__(self, review_repository: ReviewRepository, book_repository: BookRepository):
        self.review_repository = review_repository
        self.book_repository = book_repository

    def execute(self, command: DeleteReviewCommand) -> None:
        # Преобразуем в value objects
        try:
            id = ReviewId(command.id)
        except Exception as e:
            raise InvalidReviewDataError(
                f"Некорректные данные для удаления отзыва: {str(e)}"
            ) from e

        # Проверяем, существует ли отзыв
        review = self.review_repository.get_by_id(id)
        if review is None:
            raise ReviewNotFoundError(f"Отзыв с ID {id.value} не найден")

        self.review_repository.delete(review)
        book = GetBookById(book_repository=self.book_repository).execute(GetBookByIdCommand(id=review.book_id.value))
        book.decrement_ratings_count()
        self.book_repository.save(book)
