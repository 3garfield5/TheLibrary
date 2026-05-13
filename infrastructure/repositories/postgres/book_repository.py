from __future__ import annotations

from typing import Optional

from sqlalchemy import select

from thelibrary.domain.entities import Book
from thelibrary.domain.repositories.book_repository import BookRepository as BookRepositoryContract
from thelibrary.domain.value_objects import (
    Author,
    BookId,
    Rating,
    RatingsCount,
    ReleaseYear,
    Title,
)

from .database import get_session
from .models import BookModel


class PostgresBookRepository(BookRepositoryContract):
    def save(self, book: Book) -> None:
        with get_session() as session:
            db_book = session.get(BookModel, book.id.value)
            if db_book is None:
                db_book = BookModel(id=book.id.value)
                session.add(db_book)

            db_book.title = book.title.value
            db_book.author = book.author.value
            db_book.rating = book.rating.value
            db_book.ratings_count = book.ratings_count.value
            db_book.release_year = book.release_year.value

    def get_by_id(self, id: BookId) -> Optional[Book]:
        with get_session() as session:
            row = session.get(BookModel, id.value)

        if row is None:
            return None
        return self._to_entity(row)

    def get_by_title(self, title: Title) -> Optional[Book]:
        with get_session() as session:
            row = session.scalar(select(BookModel).where(BookModel.title == title.value))

        if row is None:
            return None
        return self._to_entity(row)

    def delete(self, book: Book) -> None:
        with get_session() as session:
            row = session.get(BookModel, book.id.value)
            if row is not None:
                session.delete(row)

    @staticmethod
    def _to_entity(row: BookModel) -> Book:
        return Book.create(
            id=BookId(row.id),
            title=Title(row.title),
            author=Author(row.author),
            rating=Rating(float(row.rating)),
            ratings_count=RatingsCount(row.ratings_count),
            release_year=ReleaseYear(row.release_year),
        )
