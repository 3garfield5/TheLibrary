from fastapi import APIRouter, Depends, status

from api.app.dependencies.container import (
    get_create_review,
    get_delete_review,
    get_get_review_by_id,
)
from api.app.schemas.review import ReviewResponse, to_review_response
from thelibrary.use_cases.review import (
    CreateReview,
    CreateReviewCommand,
    DeleteReview,
    DeleteReviewCommand,
    GetReviewById,
    GetReviewByIdCommand,
)

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_review(
    book_id: str,
    rating: int,
    comment: str,
    user_id: str,
    use_case: CreateReview = Depends(get_create_review),
):
    command = CreateReviewCommand(
        book_id=book_id,
        rating=rating,
        comment=comment,
        user_id=user_id,
    )
    review_id = use_case.execute(command)

    return {"review_id": review_id.value}


@router.get("/", response_model=ReviewResponse)
def get_review(
    id: str,
    use_case: GetReviewById = Depends(get_get_review_by_id),
):
    review = use_case.execute(GetReviewByIdCommand(id=id))

    return to_review_response(review)


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: str,
    user_id: str,
    use_case: DeleteReview = Depends(get_delete_review),
):
    use_case.execute(DeleteReviewCommand(id=review_id, user_id=user_id))
