from dataclasses import dataclass

from thelibrary.domain.entities import Review
from thelibrary.domain.repositories import ReviewRepository
from thelibrary.domain.value_objects import ReviewId
from thelibrary.exceptions.domain_exceptions import (
    ReviewNotFoundError,
    InvalidReviewDataError,
)


@dataclass(frozen=True)
class GetReviewByIdCommand:
    id: str


class GetReviewById:
    def __init__(self, review_repository: ReviewRepository):
        self.review_repository = review_repository

    def execute(self, command: GetReviewByIdCommand) -> Review:
        # Преобразуем в value objects
        try:
            id = ReviewId(command.id)
        except Exception as e:
            raise InvalidReviewDataError(
                f"Некорректные данные для получения отзыва: {str(e)}"
            ) from e

        # Проверяем, существует ли отзыв
        review = self.review_repository.get_by_id(id)
        if review is None:
            raise ReviewNotFoundError(f"Отзыв с ID {id.value} не найден")

        return review
