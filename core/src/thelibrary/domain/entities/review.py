from __future__ import annotations

from thelibrary.domain.value_objects import BookId, Comment, Rating, ReviewId, UserId


class Review:
    def __init__(
        self,
        id: ReviewId,
        rating: Rating,
        comment: Comment,
        book_id: BookId,
        user_id: UserId,
    ):
        self._id: ReviewId = id
        self._rating: Rating = rating
        self._comment: Comment = comment
        self._book_id: BookId = book_id
        self._user_id: UserId = user_id

    @property
    def id(self) -> ReviewId:
        return self._id

    @property
    def rating(self) -> Rating:
        return self._rating

    @property
    def comment(self) -> Comment:
        return self._comment

    @property
    def book_id(self) -> BookId:
        return self._book_id

    @property
    def user_id(self) -> UserId:
        return self._user_id

    def __str__(self) -> str:
        return f'Отзыв с оценкой {self.rating} и комментарием "{self.comment}"'

    @classmethod
    def create(
        cls,
        id: ReviewId,
        rating: Rating,
        comment: Comment,
        book_id: BookId,
        user_id: UserId,
    ) -> Review:
        return cls(
            id=id, rating=rating, comment=comment, book_id=book_id, user_id=user_id
        )

    # fill with methods
