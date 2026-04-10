from __future__ import annotations

from typing import Protocol

from .contracts import LLMLogRecord, RecommendationInput, RecommendationResult


class LLMProvider(Protocol):
    def generate(self, payload: RecommendationInput) -> RecommendationResult:
        ...


class LLMLogRepository(Protocol):
    def save(self, record: LLMLogRecord) -> None:
        ...

    def list_recent(self, limit: int = 100) -> list[LLMLogRecord]:
        ...
