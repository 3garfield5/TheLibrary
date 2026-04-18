from __future__ import annotations

from dataclasses import dataclass, field

from thelibrary.domain.repositories.llm_repository import (
    LLMRecommendLike,
    LLMRecommendRequest,
    LLMRecommendResponse,
    LLMRecommendReview,
    LLMRepository,
)
from thelibrary.exceptions.domain_exceptions import InvalidLLMRequestError


@dataclass(frozen=True)
class RecommendBooksCommand:
    user_id: str
    likes: tuple[LLMRecommendLike, ...] = field(default_factory=tuple)
    reviews: tuple[LLMRecommendReview, ...] = field(default_factory=tuple)
    community_reviews: tuple[LLMRecommendReview, ...] = field(default_factory=tuple)
    limit: int = 5
    language: str = "ru"


class RecommendBooks:
    def __init__(self, llm_repository: LLMRepository):
        self.llm_repository = llm_repository

    def execute(self, command: RecommendBooksCommand) -> LLMRecommendResponse:
        user_id = command.user_id.strip()
        if not user_id:
            raise InvalidLLMRequestError("user_id is required")
        if command.limit <= 0:
            raise InvalidLLMRequestError("limit must be greater than 0")
        if not command.likes and not command.reviews:
            raise InvalidLLMRequestError("likes or reviews are required")

        request = LLMRecommendRequest(
            user_id=user_id,
            likes=command.likes,
            reviews=command.reviews,
            community_reviews=command.community_reviews,
            limit=command.limit,
            language=command.language,
        )
        return self.llm_repository.recommend(request)
