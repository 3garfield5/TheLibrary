from __future__ import annotations

import json

from .contracts import Recommendation
from .exceptions import LLMProviderError


def parse_recommendations_json(raw_response: str) -> tuple[Recommendation, ...]:
    payload = _load_json(raw_response)

    items = payload.get("recommendations")
    if not isinstance(items, list):
        raise LLMProviderError("missing recommendations list")

    recommendations: list[Recommendation] = []
    for item in items:
        if not isinstance(item, dict):
            continue

        title = str(item.get("title", "")).strip()
        author = str(item.get("author", "")).strip()
        reason = str(item.get("reason", "")).strip()
        if not title or not author or not reason:
            continue

        confidence_value = item.get("confidence", 0.5)
        try:
            confidence = float(confidence_value)
        except (TypeError, ValueError):
            confidence = 0.5

        recommendations.append(
            Recommendation(
                title=title,
                author=author,
                reason=reason,
                confidence=min(max(confidence, 0.0), 1.0),
            )
        )

    return tuple(recommendations)


def _load_json(raw_response: str) -> dict:
    try:
        data = json.loads(raw_response)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass

    start = raw_response.find("{")
    end = raw_response.rfind("}")
    if start != -1 and end != -1 and end > start:
        fragment = raw_response[start : end + 1]
        try:
            data = json.loads(fragment)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            pass

    raise LLMProviderError("invalid JSON response")
