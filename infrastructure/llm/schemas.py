from __future__ import annotations

from pydantic import BaseModel, Field


class LikeIn(BaseModel):
    title: str
    author: str
    genres: list[str] = Field(default_factory=list)


class ReviewIn(BaseModel):
    title: str
    author: str
    rating: float
    comment: str = ""


class RecommendIn(BaseModel):
    user_id: str
    likes: list[LikeIn] = Field(default_factory=list)
    reviews: list[ReviewIn] = Field(default_factory=list)
    community_reviews: list[ReviewIn] = Field(default_factory=list)
    limit: int = 5
    language: str = "ru"


class RecommendationOut(BaseModel):
    book_id: str
    title: str
    author: str
    reason: str
    confidence: float
    score: float
    social_score: float


class RecommendOut(BaseModel):
    model_name: str
    profile_model_name: str
    recommendations: list[RecommendationOut]


class ChatIn(BaseModel):
    user_id: str
    message: str
    language: str = "ru"
    system_prompt: str | None = None


class ChatOut(BaseModel):
    model_name: str
    response: str
