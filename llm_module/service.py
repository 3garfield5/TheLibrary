from __future__ import annotations

from datetime import datetime, timezone

from .contracts import LLMLogRecord, Recommendation, RecommendationInput, RecommendationResult
from .exceptions import LLMValidationError
from .ports import LLMLogRepository, LLMProvider


class RecommendationService:
    def __init__(self, provider: LLMProvider, logs: LLMLogRepository):
        self._provider = provider
        self._logs = logs

    def recommend(self, payload: RecommendationInput) -> RecommendationResult:
        self._validate(payload)

        started_at = datetime.now(timezone.utc)
        raw_result = self._provider.generate(payload)
        result = self._postprocess(raw_result, payload)

        self._logs.save(
            LLMLogRecord(
                created_at=started_at,
                model_name=result.model_name,
                recommendations_count=len(result.recommendations),
                latency_ms=int((datetime.now(timezone.utc) - started_at).total_seconds() * 1000),
            )
        )

        return result

    def _validate(self, payload: RecommendationInput) -> None:
        if not payload.user_id.strip() or not payload.list_id.strip():
            raise LLMValidationError("user_id and list_id must not be empty")
        if payload.limit < 1:
            raise LLMValidationError("limit must be at least 1")
        if not payload.seeds:
            raise LLMValidationError("seeds must contain at least one book")

    def _postprocess(self, result: RecommendationResult, payload: RecommendationInput) -> RecommendationResult:
        existing = {(seed.title.strip().casefold(), seed.author.strip().casefold()) for seed in payload.seeds}
        seen: set[tuple[str, str]] = set()
        cleaned: list[Recommendation] = []

        for rec in result.recommendations:
            title = rec.title.strip()
            author = rec.author.strip()
            reason = rec.reason.strip()
            key = (title.casefold(), author.casefold())

            if not title or not author:
                continue
            if key in existing or key in seen:
                continue
            if self._is_low_quality_reason(reason):
                continue

            cleaned.append(
                Recommendation(
                    title=title,
                    author=author,
                    reason=reason,
                    confidence=min(max(rec.confidence, 0.0), 1.0),
                )
            )
            seen.add(key)

            if len(cleaned) >= payload.limit:
                break

        return RecommendationResult(recommendations=tuple(cleaned), model_name=result.model_name)

    def _is_low_quality_reason(self, reason: str) -> bool:
        normalized = reason.strip()
        lowered = normalized.casefold()
        if not normalized:
            return True
        if normalized in {"...", "-", "n/a", "none"}:
            return True
        if len(normalized) < 24:
            return True

        generic_markers = (
            "классическим примером",
            "просто пример",
            "является примером",
            "this is a classic example",
            "is a classic example",
            "this book is an example",
        )
        if any(marker in lowered for marker in generic_markers):
            return True
        return False
