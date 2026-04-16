from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CatalogBook:
    id: str
    title: str
    author: str
    genres: tuple[str, ...]
    summary: str


@dataclass(frozen=True, slots=True)
class RecommendRequest:
    user_id: str
    likes: tuple[dict, ...]
    reviews: tuple[dict, ...]
    community_reviews: tuple[dict, ...]
    limit: int
    language: str


@dataclass(frozen=True, slots=True)
class RecommendationItem:
    book_id: str
    title: str
    author: str
    reason: str
    confidence: float
    score: float
    social_score: float


@dataclass(frozen=True, slots=True)
class RecommendResult:
    model_name: str
    profile_model_name: str
    embedding: tuple[float, ...]
    recommendations: tuple[RecommendationItem, ...]
