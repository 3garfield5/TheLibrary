from pydantic import BaseModel


class ReviewResponse(BaseModel):
    id: str
    rating: int
    comment: str
    book_id: str
    user_id: str


def to_review_response(review) -> ReviewResponse:
    return ReviewResponse(
        id=str(review.id.value),
        rating=review.rating.value,
        comment=review.comment.value,
        book_id=str(review.book_id.value),
        user_id=str(review.user_id.value)
    )
