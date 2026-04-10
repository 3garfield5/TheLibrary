from __future__ import annotations

from .contracts import RecommendationInput


PROMPT_VERSION = "v2"


def build_system_prompt(language: str) -> str:
    if language.casefold().startswith("ru"):
        return (
            "Ты книжный ассистент. Ответ только в JSON, без дополнительного текста. "
            "Не возвращай книги из входного списка пользователя."
        )
    return (
        "You are a book assistant. Return JSON only with no extra text. "
        "Do not return books that are already in the user's input list."
    )


def build_user_prompt(payload: RecommendationInput) -> str:
    lines = [
        'Return JSON: {"recommendations":[{"title":"...","author":"...","reason":"...","confidence":0.0}]}',
        f"Max recommendations: {payload.limit}",
        "Rules:",
        "- Recommend only new books, never repeat input books.",
        "- reason must be specific (theme, tone, pacing, style, conflict), 12-40 words.",
        "- confidence must be between 0.3 and 0.95.",
        "- If unsure, return fewer recommendations instead of generic placeholders.",
        "User books:",
    ]

    for i, seed in enumerate(payload.seeds, start=1):
        genres = ", ".join(seed.genres) if seed.genres else "-"
        lines.append(f"{i}. title={seed.title}; author={seed.author}; genres={genres}")

    return "\n".join(lines)
