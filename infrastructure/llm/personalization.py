from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from statistics import fmean
from typing import Any

from pydantic import BaseModel, Field

from .exceptions import LLMProviderError, LLMValidationError
from .personalization_contracts import CatalogBook, RecommendRequest, RecommendResult, RecommendationItem


class PickSchema(BaseModel):
    book_id: str
    reason: str
    confidence: float = 0.5


class PicksEnvelope(BaseModel):
    recommendations: list[PickSchema] = Field(default_factory=list)


def _book_text(book: CatalogBook) -> str:
    return f"{book.title}\n{book.author}\n{' '.join(book.genres)}\n{book.summary}".strip()


def _book_key(title: str, author: str) -> tuple[str, str]:
    return title.strip().casefold(), author.strip().casefold()


class Catalog:
    def __init__(self, books: tuple[CatalogBook, ...]):
        self.books = books

    @classmethod
    def from_json(cls, path: Path) -> "Catalog":
        raw = json.loads(path.read_text(encoding="utf-8"))
        books: list[CatalogBook] = []
        for item in raw:
            if not isinstance(item, dict):
                continue
            books.append(
                CatalogBook(
                    id=str(item.get("id", "")).strip(),
                    title=str(item.get("title", "")).strip(),
                    author=str(item.get("author", "")).strip(),
                    genres=tuple(str(x).strip() for x in item.get("genres", []) if str(x).strip()),
                    summary=str(item.get("summary", "")).strip(),
                )
            )
        books = [b for b in books if b.id and b.title and b.author and b.summary]
        return cls(tuple(books))


class FaissRetriever:
    def __init__(self, catalog: Catalog, index_path: Path | None, meta_path: Path | None, enabled: bool):
        self.enabled = False
        self.dimension = 0
        self._index: Any | None = None
        self._np: Any | None = None
        self._faiss: Any | None = None
        self._book_refs: list[CatalogBook] = []

        if not enabled or not index_path or not meta_path:
            return
        if not index_path.exists() or not meta_path.exists():
            return

        try:
            import faiss
            import numpy as np
        except ModuleNotFoundError:
            return

        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        ids = meta.get("book_ids", [])
        self.dimension = int(meta.get("dimension", 0))
        if not ids or self.dimension <= 0:
            return

        books_by_id = {book.id: book for book in catalog.books}
        refs = [books_by_id[x] for x in ids if isinstance(x, str) and x in books_by_id]
        if not refs:
            return

        self._index = faiss.read_index(str(index_path))
        self._np = np
        self._faiss = faiss
        self._book_refs = refs
        self.enabled = True

    def search(self, vector: tuple[float, ...], top_k: int) -> list[tuple[CatalogBook, float]]:
        if not self.enabled or self._index is None or self._np is None or self._faiss is None:
            return []
        if len(vector) != self.dimension:
            return []

        query = self._np.array([list(vector)], dtype="float32")
        self._faiss.normalize_L2(query)
        scores, ids = self._index.search(query, max(top_k, 1))

        out: list[tuple[CatalogBook, float]] = []
        for score, idx in zip(scores[0], ids[0]):
            if idx < 0 or idx >= len(self._book_refs):
                continue
            out.append((self._book_refs[idx], float(score)))
        return out


class SimpleRecommenderService:
    def __init__(
        self,
        catalog: Catalog,
        transport,
        llm_model_name: str,
        profile_model_name: str,
        profile_embedding_model: str,
        use_faiss: bool,
        faiss_index_path: Path | None = None,
        faiss_meta_path: Path | None = None,
    ):
        self.catalog = catalog
        self.transport = transport
        self.llm_model_name = llm_model_name
        self.profile_model_name = profile_model_name

        try:
            import numpy as np
            from sentence_transformers import SentenceTransformer
        except ModuleNotFoundError as exc:
            raise LLMProviderError("sentence-transformers and numpy are required") from exc

        self._np = np
        self.encoder = SentenceTransformer(profile_embedding_model)
        self.retriever = FaissRetriever(catalog, faiss_index_path, faiss_meta_path, use_faiss)

        self._book_refs: tuple[CatalogBook, ...] = catalog.books
        if self._book_refs:
            book_texts = [_book_text(book) for book in self._book_refs]
            self._book_matrix = self.encoder.encode(
                book_texts,
                normalize_embeddings=True,
                convert_to_numpy=True,
            ).astype("float32")
        else:
            self._book_matrix = self._np.zeros((0, 0), dtype="float32")

    def _user_embedding(self, payload: RecommendRequest) -> tuple[float, ...]:
        lines: list[str] = [f"user_id={payload.user_id}"]
        for like in payload.likes:
            lines.append(f"like {like.get('title','')} {like.get('author','')} {' '.join(like.get('genres', []))}")
        for review in payload.reviews:
            lines.append(
                f"review {review.get('title','')} {review.get('author','')} rating={review.get('rating', 0)} {review.get('comment', '')}"
            )
        text = "\n".join(lines)
        emb = self.encoder.encode(text, normalize_embeddings=True, convert_to_numpy=True)
        return tuple(float(x) for x in emb)

    def _social_map(self, reviews: tuple[dict, ...]) -> dict[tuple[str, str], float]:
        buckets: defaultdict[tuple[str, str], list[float]] = defaultdict(list)
        for r in reviews:
            key = _book_key(str(r.get("title", "")), str(r.get("author", "")))
            buckets[key].append(float(r.get("rating", 0.0)))

        out: dict[tuple[str, str], float] = {}
        for key, ratings in buckets.items():
            if not ratings:
                continue
            avg = fmean(ratings)
            out[key] = (avg - 3.0) / 2.0 * 0.15
        return out

    def _retrieve(self, user_vector: tuple[float, ...], limit: int) -> list[tuple[CatalogBook, float]]:
        if self.retriever.enabled:
            hits = self.retriever.search(user_vector, top_k=max(limit * 4, 20))
            if hits:
                return hits

        if self._book_matrix.size == 0:
            return []

        query = self._np.asarray(user_vector, dtype="float32")
        if query.shape[0] != self._book_matrix.shape[1]:
            return []

        # Embeddings are normalized, so cosine similarity equals dot product.
        scores = self._book_matrix @ query
        top_k = min(max(limit * 4, 20), scores.shape[0])
        if top_k <= 0:
            return []

        if top_k == scores.shape[0]:
            top_idx = self._np.argsort(scores)[::-1]
        else:
            candidate_idx = self._np.argpartition(-scores, top_k - 1)[:top_k]
            top_idx = candidate_idx[self._np.argsort(scores[candidate_idx])[::-1]]

        return [(self._book_refs[int(idx)], float(scores[int(idx)])) for idx in top_idx]

    def _pick_with_llm(
        self,
        language: str,
        user_vector: tuple[float, ...],
        candidates: list[tuple[CatalogBook, float]],
        excluded: set[tuple[str, str]],
        limit: int,
    ) -> list[PickSchema]:
        system = (
            "Ты рекомендуешь книги. Верни только JSON {\"recommendations\":[{\"book_id\":\"...\",\"reason\":\"...\",\"confidence\":0.0}]}"
            if language.casefold().startswith("ru")
            else "You recommend books. Return JSON only {\"recommendations\":[{\"book_id\":\"...\",\"reason\":\"...\",\"confidence\":0.0}]}"
        )
        lines = [
            f"Need {limit} recommendations",
            f"User embedding dim={len(user_vector)}",
            "Already known books:",
        ]
        for t, a in sorted(excluded):
            lines.append(f"- {t} / {a}")
        lines.append("Candidates:")
        for book, sim in candidates:
            lines.append(
                f"book_id={book.id}; title={book.title}; author={book.author}; genres={', '.join(book.genres)}; sim={round(sim,4)}; summary={book.summary}"
            )

        raw = self.transport(system, "\n".join(lines), PicksEnvelope)
        return list(PicksEnvelope.model_validate(raw).recommendations)

    def recommend(self, payload: RecommendRequest) -> RecommendResult:
        if not payload.user_id.strip():
            raise LLMValidationError("user_id is required")
        if not payload.likes and not payload.reviews:
            raise LLMValidationError("likes or reviews are required")

        user_vector = self._user_embedding(payload)
        excluded = set()
        for like in payload.likes:
            excluded.add(_book_key(str(like.get("title", "")), str(like.get("author", ""))))
        for review in payload.reviews:
            excluded.add(_book_key(str(review.get("title", "")), str(review.get("author", ""))))

        social = self._social_map(payload.community_reviews)
        base = self._retrieve(user_vector, payload.limit)

        prepared: list[tuple[CatalogBook, float, float]] = []
        for book, sim in base:
            key = _book_key(book.title, book.author)
            if key in excluded:
                continue
            social_score = social.get(key, 0.0)
            prepared.append((book, sim, sim + social_score))

        prepared.sort(key=lambda x: x[2], reverse=True)
        top = [(x[0], x[2]) for x in prepared[:12]]

        picks = self._pick_with_llm(payload.language, user_vector, top, excluded, payload.limit)
        by_id = {book.id: (book, score) for book, score in top}

        items: list[RecommendationItem] = []
        used: set[str] = set()
        for pick in picks:
            if pick.book_id in used:
                continue
            pair = by_id.get(pick.book_id)
            if pair is None:
                continue
            book, score = pair
            social_score = social.get(_book_key(book.title, book.author), 0.0)
            items.append(
                RecommendationItem(
                    book_id=book.id,
                    title=book.title,
                    author=book.author,
                    reason=pick.reason.strip() or "Подходит по вкусу",
                    confidence=max(0.0, min(1.0, float(pick.confidence))),
                    score=round(score, 4),
                    social_score=round(social_score, 4),
                )
            )
            used.add(pick.book_id)
            if len(items) >= payload.limit:
                break

        if not items:
            for book, score in top[: payload.limit]:
                social_score = social.get(_book_key(book.title, book.author), 0.0)
                items.append(
                    RecommendationItem(
                        book_id=book.id,
                        title=book.title,
                        author=book.author,
                        reason="Подобрано по похожести профиля",
                        confidence=0.5,
                        score=round(score, 4),
                        social_score=round(social_score, 4),
                    )
                )

        return RecommendResult(
            model_name=self.llm_model_name,
            profile_model_name=self.profile_model_name,
            embedding=user_vector,
            recommendations=tuple(items),
        )


def load_catalog(path: Path | None = None) -> Catalog:
    catalog_path = path or (Path(__file__).with_name("catalog_data") / "books_40.json")
    return Catalog.from_json(catalog_path)
