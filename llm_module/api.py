from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException

from .exceptions import LLMProviderError, LLMValidationError
from .personalization import SimpleRecommenderService, load_catalog
from .personalization_contracts import RecommendRequest
from .schemas import ChatIn, ChatOut, RecommendIn, RecommendOut, RecommendationOut
from .transports import LangChainChatOpenAITransport


def build_transport() -> tuple[LangChainChatOpenAITransport, str]:
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
    return transport, model


def build_recommender() -> tuple[SimpleRecommenderService, LangChainChatOpenAITransport, str]:
    transport, llm_model = build_transport()

    use_faiss = os.getenv("USE_FAISS", "false").strip().casefold() in {"1", "true", "yes", "on"}
    index_path = os.getenv("FAISS_INDEX_PATH")
    meta_path = os.getenv("FAISS_META_PATH")

    service = SimpleRecommenderService(
        catalog=load_catalog(),
        transport=transport,
        llm_model_name=f"{llm_model}:recommend",
        profile_model_name="sentence-transformers-profile",
        profile_embedding_model=os.getenv(
            "PROFILE_EMBEDDING_MODEL",
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        ),
        use_faiss=use_faiss,
        faiss_index_path=Path(index_path) if index_path else None,
        faiss_meta_path=Path(meta_path) if meta_path else None,
    )
    return service, transport, llm_model


recommender: SimpleRecommenderService | None = None
chat_transport: LangChainChatOpenAITransport | None = None
chat_model: str = os.getenv("LLM_MODEL", "qwen2.5:1.5b")
initialization_error: str | None = None

try:
    recommender, chat_transport, chat_model = build_recommender()
except Exception as exc:
    initialization_error = str(exc)

app = FastAPI(title="TheLibrary LLM API", version="4.0.0")


@app.get("/health")
def health() -> dict[str, bool]:
    return {"ok": True}


@app.post("/recommend", response_model=RecommendOut)
def recommend(payload: RecommendIn) -> RecommendOut:
    if initialization_error:
        raise HTTPException(status_code=503, detail=initialization_error)
    assert recommender is not None

    request = RecommendRequest(
        user_id=payload.user_id,
        likes=tuple(item.model_dump() for item in payload.likes),
        reviews=tuple(item.model_dump() for item in payload.reviews),
        community_reviews=tuple(item.model_dump() for item in payload.community_reviews),
        limit=payload.limit,
        language=payload.language,
    )

    try:
        result = recommender.recommend(request)
    except LLMValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except LLMProviderError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return RecommendOut(
        model_name=result.model_name,
        profile_model_name=result.profile_model_name,
        recommendations=[
            RecommendationOut(
                book_id=item.book_id,
                title=item.title,
                author=item.author,
                reason=item.reason,
                confidence=item.confidence,
                score=item.score,
                social_score=item.social_score,
            )
            for item in result.recommendations
        ],
    )


@app.post("/chat", response_model=ChatOut)
def chat(payload: ChatIn) -> ChatOut:
    if initialization_error:
        raise HTTPException(status_code=503, detail=initialization_error)
    assert chat_transport is not None

    if not payload.user_id.strip() or not payload.message.strip():
        raise HTTPException(status_code=400, detail="user_id and message are required")

    system_prompt = payload.system_prompt
    if not system_prompt or not system_prompt.strip():
        system_prompt = (
            "Ты дружелюбный книжный ассистент. Отвечай коротко и по делу."
            if payload.language.casefold().startswith("ru")
            else "You are a friendly book assistant. Keep answers concise."
        )

    try:
        response = chat_transport.chat(system_prompt, payload.message)
    except LLMProviderError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return ChatOut(model_name=chat_model, response=response)


def main() -> None:
    import uvicorn

    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "8000"))
    uvicorn.run("llm_module.api:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    main()
