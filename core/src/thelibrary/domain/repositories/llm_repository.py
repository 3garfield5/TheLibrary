from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class LLMRecommendLike:
    title: str
    author: str
    genres: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class LLMRecommendReview:
    title: str
    author: str
    rating: float
    comment: str = ""


@dataclass(frozen=True, slots=True)
class LLMRecommendation:
    book_id: str
    title: str
    author: str
    reason: str
    confidence: float
    score: float
    social_score: float


@dataclass(frozen=True, slots=True)
class LLMRecommendRequest:
    user_id: str
    likes: tuple[LLMRecommendLike, ...]
    reviews: tuple[LLMRecommendReview, ...]
    community_reviews: tuple[LLMRecommendReview, ...]
    limit: int
    language: str


@dataclass(frozen=True, slots=True)
class LLMRecommendResponse:
    model_name: str
    profile_model_name: str
    recommendations: tuple[LLMRecommendation, ...]


@dataclass(frozen=True, slots=True)
class LLMChatRequest:
    user_id: str
    message: str
    language: str
    system_prompt: str | None = None


@dataclass(frozen=True, slots=True)
class LLMChatResponse:
    model_name: str
    response: str


class LLMRepository(ABC):
    @abstractmethod
    def recommend(self, request: LLMRecommendRequest) -> LLMRecommendResponse:
        pass

    @abstractmethod
    def chat(self, request: LLMChatRequest) -> LLMChatResponse:
        pass
