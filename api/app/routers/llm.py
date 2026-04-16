from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from api.app.dependencies.container import (
    get_chat_with_assistant,
    get_llm_initialization_error,
    get_recommend_books,
)
from infrastructure.llm.exceptions import LLMProviderError, LLMValidationError
from infrastructure.llm.schemas import (
    ChatIn,
    ChatOut,
    RecommendIn,
    RecommendOut,
    RecommendationOut,
)
from thelibrary.domain.repositories.llm_repository import LLMRecommendLike, LLMRecommendReview
from thelibrary.exceptions.domain_exceptions import InvalidLLMRequestError
from thelibrary.use_cases.llm import (
    ChatWithAssistant,
    ChatWithAssistantCommand,
    RecommendBooks,
    RecommendBooksCommand,
)

router = APIRouter(prefix="/llm", tags=["llm"])


@router.post("/recommend", response_model=RecommendOut)
def recommend(
    payload: RecommendIn,
    use_case: RecommendBooks | None = Depends(get_recommend_books),
    initialization_error: str | None = Depends(get_llm_initialization_error),
) -> RecommendOut:
    if initialization_error:
        raise HTTPException(status_code=503, detail=initialization_error)
    if use_case is None:
        raise HTTPException(status_code=503, detail="LLM module is not initialized")

    command = RecommendBooksCommand(
        user_id=payload.user_id,
        likes=tuple(
            LLMRecommendLike(title=item.title, author=item.author, genres=tuple(item.genres))
            for item in payload.likes
        ),
        reviews=tuple(
            LLMRecommendReview(
                title=item.title,
                author=item.author,
                rating=item.rating,
                comment=item.comment,
            )
            for item in payload.reviews
        ),
        community_reviews=tuple(
            LLMRecommendReview(
                title=item.title,
                author=item.author,
                rating=item.rating,
                comment=item.comment,
            )
            for item in payload.community_reviews
        ),
        limit=payload.limit,
        language=payload.language,
    )

    try:
        result = use_case.execute(command)
    except (InvalidLLMRequestError, LLMValidationError) as exc:
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


@router.post("/chat", response_model=ChatOut)
def chat(
    payload: ChatIn,
    use_case: ChatWithAssistant | None = Depends(get_chat_with_assistant),
    initialization_error: str | None = Depends(get_llm_initialization_error),
) -> ChatOut:
    if initialization_error:
        raise HTTPException(status_code=503, detail=initialization_error)
    if use_case is None:
        raise HTTPException(status_code=503, detail="LLM module is not initialized")

    command = ChatWithAssistantCommand(
        user_id=payload.user_id,
        message=payload.message,
        language=payload.language,
        system_prompt=payload.system_prompt,
    )

    try:
        result = use_case.execute(command)
    except InvalidLLMRequestError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except LLMProviderError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return ChatOut(model_name=result.model_name, response=result.response)
