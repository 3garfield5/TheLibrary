from __future__ import annotations

from sqlalchemy import (
    Boolean,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    author: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    ratings_count: Mapped[int] = mapped_column(Integer, nullable=False)
    release_year: Mapped[int] = mapped_column(Integer, nullable=False)


class ReviewModel(Base):
    __tablename__ = "reviews"
    __table_args__ = (UniqueConstraint("book_id", "user_id", name="uq_reviews_book_user"),)

    id: Mapped[str] = mapped_column(String, primary_key=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    book_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("books.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )


class UserListModel(Base):
    __tablename__ = "user_lists"
    __table_args__ = (
        UniqueConstraint("user_id", "title", name="uq_user_lists_user_title"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    is_private: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    user_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )


class UserListBookModel(Base):
    __tablename__ = "user_list_books"
    __table_args__ = (
        UniqueConstraint("user_list_id", "book_id", name="uq_user_list_books_list_book"),
    )

    user_list_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("user_lists.id", ondelete="CASCADE"),
        primary_key=True,
    )
    book_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("books.id", ondelete="CASCADE"),
        primary_key=True,
    )
