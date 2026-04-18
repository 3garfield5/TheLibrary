from __future__ import annotations

import os
from pathlib import Path

from thelibrary.domain.repositories.llm_repository import (
    LLMChatRequest,
    LLMChatResponse,
    LLMRecommendation,
    LLMRecommendRequest,
    LLMRecommendResponse,
    LLMRepository,
)

from .personalization import SimpleRecommenderService, load_catalog
from .personalization_contracts import RecommendRequest
from .transports import LangChainChatOpenAITransport


class LLMModuleRepository(LLMRepository):
    def __init__(
        self,
        recommender: SimpleRecommenderService,
        chat_transport: LangChainChatOpenAITransport,
        chat_model: str,
    ):
        self._recommender = recommender
        self._chat_transport = chat_transport
        self._chat_model = chat_model

    @staticmethod
    def _to_recommend_payload(request: LLMRecommendRequest) -> RecommendRequest:
        return RecommendRequest(
            user_id=request.user_id,
            likes=tuple(
                {
                    "title": item.title,
                    "author": item.author,
                    "genres": list(item.genres),
                }
                for item in request.likes
            ),
            reviews=tuple(
                {
                    "title": item.title,
                    "author": item.author,
                    "rating": item.rating,
                    "comment": item.comment,
                }
                for item in request.reviews
            ),
            community_reviews=tuple(
                {
                    "title": item.title,
                    "author": item.author,
                    "rating": item.rating,
                    "comment": item.comment,
                }
                for item in request.community_reviews
            ),
            limit=request.limit,
            language=request.language,
        )

    def recommend(self, request: LLMRecommendRequest) -> LLMRecommendResponse:
        result = self._recommender.recommend(self._to_recommend_payload(request))
        return LLMRecommendResponse(
            model_name=result.model_name,
            profile_model_name=result.profile_model_name,
            recommendations=tuple(
                LLMRecommendation(
                    book_id=item.book_id,
                    title=item.title,
                    author=item.author,
                    reason=item.reason,
                    confidence=item.confidence,
                    score=item.score,
                    social_score=item.social_score,
                )
                for item in result.recommendations
            ),
        )

    def chat(self, request: LLMChatRequest) -> LLMChatResponse:
        system_prompt = request.system_prompt
        if not system_prompt or not system_prompt.strip():
            system_prompt = (
                "Ты дружелюбный книжный ассистент. Отвечай коротко и по делу."
                if request.language.casefold().startswith("ru")
                else "You are a friendly book assistant. Keep answers concise."
            )

        response = self._chat_transport.chat(system_prompt, request.message)
        return LLMChatResponse(model_name=self._chat_model, response=response)


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

    use_faiss = os.getenv("USE_FAISS", "false").strip().casefold() in {
        "1",
        "true",
        "yes",
        "on",
    }
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


def build_llm_repository() -> LLMRepository:
    recommender, chat_transport, chat_model = build_recommender()
    return LLMModuleRepository(
        recommender=recommender,
        chat_transport=chat_transport,
        chat_model=chat_model,
    )


__all__ = ["LLMModuleRepository", "build_llm_repository", "build_recommender", "build_transport"]
