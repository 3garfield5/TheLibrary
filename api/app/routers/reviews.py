from fastapi import APIRouter, Depends

from api.app.dependencies.container import get_create_review, get_get_review_by_id
from thelibrary.use_cases.review import CreateReview, CreateReviewCommand, GetReviewById, GetReviewByIdCommand
from api.app.schemas.review import ReviewResponse, to_review_response

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post("/")
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

    return {"review_id": str(review_id)}

@router.get("/", response_model=ReviewResponse)
def get_review(
    id: str,
    use_case: GetReviewById = Depends(get_get_review_by_id),
):
    command = GetReviewByIdCommand(
        id=id
    )
    review = use_case.execute(command)

    return to_review_response(review)
