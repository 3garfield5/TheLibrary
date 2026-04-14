from __future__ import annotations

from typing import Callable

from pydantic import BaseModel, Field

from ..contracts import Recommendation, RecommendationInput, RecommendationResult
from ..prompting import build_system_prompt, build_user_prompt


class RecommendationSchema(BaseModel):
    title: str
    author: str
    reason: str
    confidence: float = 0.5


class RecommendationEnvelopeSchema(BaseModel):
    recommendations: list[RecommendationSchema] = Field(default_factory=list)


ChatTransport = Callable[[str, str, type], RecommendationEnvelopeSchema]


class ListBasedLLMProvider:
    def __init__(self, transport: ChatTransport, model_name: str = "llm-chat-model"):
        self._transport = transport
        self.model_name = model_name

    def generate(self, payload: RecommendationInput) -> RecommendationResult:
        system_prompt = build_system_prompt(payload.language)
        user_prompt = build_user_prompt(payload)
        raw_structured = self._transport(
            system_prompt, user_prompt, RecommendationEnvelopeSchema
        )
        structured = RecommendationEnvelopeSchema.model_validate(raw_structured)

        return RecommendationResult(
            recommendations=tuple(
                Recommendation(
                    title=item.title,
                    author=item.author,
                    reason=item.reason,
                    confidence=item.confidence,
                )
                for item in structured.recommendations
            ),
            model_name=self.model_name,
        )
