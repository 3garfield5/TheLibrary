from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .contracts import BookSeed, RecommendationInput
from .exceptions import LLMProviderError, LLMValidationError
from .logging import InMemoryLLMLogRepository
from .providers import ListBasedLLMProvider
from .service import RecommendationService
from .transports import LangChainChatOpenAITransport


class SeedIn(BaseModel):
    title: str
    author: str
    genres: list[str] = Field(default_factory=list)


class RecommendIn(BaseModel):
    user_id: str
    list_id: str
    seeds: list[SeedIn]
    limit: int = 5
    language: str = "ru"


class RecommendationOut(BaseModel):
    title: str
    author: str
    reason: str
    confidence: float


class RecommendOut(BaseModel):
    model_name: str
    recommendations: list[RecommendationOut]


def build_service() -> RecommendationService:
    model = os.getenv("LLM_MODEL", "qwen2.5:1.5b")
    base_url = os.getenv("OPENAI_BASE_URL")
    if not base_url:
        ollama_base = (os.getenv("OLLAMA_BASE_URL") or "").rstrip("/")
        base_url = f"{ollama_base}/v1" if ollama_base else None

    transport = LangChainChatOpenAITransport(
        model=model,
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=base_url,
    )

    provider = ListBasedLLMProvider(transport=transport, model_name=model)
    return RecommendationService(provider=provider, logs=InMemoryLLMLogRepository())


service = build_service()
app = FastAPI(title="TheLibrary LLM API", version="1.0.0")


@app.get("/health")
def health() -> dict[str, bool]:
    return {"ok": True}


@app.post("/recommend", response_model=RecommendOut)
def recommend(payload: RecommendIn) -> RecommendOut:
    request = RecommendationInput(
        user_id=payload.user_id,
        list_id=payload.list_id,
        seeds=tuple(BookSeed(title=seed.title, author=seed.author, genres=tuple(seed.genres)) for seed in payload.seeds),
        limit=payload.limit,
        language=payload.language,
    )

    try:
        result = service.recommend(request)
    except (LLMValidationError, LLMProviderError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return RecommendOut(
        model_name=result.model_name,
        recommendations=[
            RecommendationOut(
                title=rec.title,
                author=rec.author,
                reason=rec.reason,
                confidence=rec.confidence,
            )
            for rec in result.recommendations
        ],
    )


def main() -> None:
    import uvicorn

    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "8000"))
    uvicorn.run("llm_module.api:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    main()
