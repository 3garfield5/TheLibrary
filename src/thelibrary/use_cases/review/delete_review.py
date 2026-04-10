from dataclasses import dataclass

from thelibrary.domain.repositories.review_repository import ReviewRepository
from thelibrary.domain.value_objects import ReviewId
from thelibrary.exceptions.domain_exceptions import (
    InvalidReviewDataError,
    ReviewNotFoundError,
)


@dataclass(frozen=True)
class DeleteReviewCommand:
    id: str


class DeleteReview:
    def __init__(self, review_repository: ReviewRepository):
        self.review_repository = review_repository

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
