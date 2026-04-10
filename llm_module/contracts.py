from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class BookSeed:
    title: str
    author: str
    genres: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class RecommendationInput:
    user_id: str
    list_id: str
    seeds: tuple[BookSeed, ...]
    limit: int = 5
    language: str = "ru"


@dataclass(frozen=True, slots=True)
class Recommendation:
    title: str
    author: str
    reason: str
    confidence: float = 0.5


@dataclass(frozen=True, slots=True)
class RecommendationResult:
    recommendations: tuple[Recommendation, ...]
    model_name: str


@dataclass(frozen=True, slots=True)
class LLMLogRecord:
    created_at: datetime
    model_name: str
    recommendations_count: int
    latency_ms: int
