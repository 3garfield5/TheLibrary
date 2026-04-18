from __future__ import annotations

from thelibrary.domain.value_objects import (
    Author,
    BookId,
    Rating,
    RatingsCount,
    ReleaseYear,
    Title,
    ReviewRating
)


class Book:
    def __init__(
        self,
        id: BookId,
        title: Title,
        author: Author,
        rating: Rating,
        ratings_count: RatingsCount,
        release_year: ReleaseYear,
    ):
        self._id: BookId = id
        self._title: Title = title
        self._author: Author = author
        self._rating: Rating = rating
        self._ratings_count: RatingsCount = ratings_count
        self._release_year: ReleaseYear = release_year

    @property
    def id(self) -> BookId:
        return self._id

    @property
    def title(self) -> Title:
        return self._title

    @property
    def author(self) -> Author:
        return self._author

    @property
    def rating(self) -> Rating:
        return self._rating

    @property
    def ratings_count(self) -> RatingsCount:
        return self._ratings_count
    
    def increment_ratings_count(self) -> None:
        self._ratings_count = RatingsCount(self._ratings_count.value + 1)

    def decrement_ratings_count(self) -> None:
        self._ratings_count = RatingsCount(self._ratings_count.value - 1)

    def update_rating(self, review_rating: ReviewRating) -> None:
        self._rating = Rating((self._rating.value * self._ratings_count.value + review_rating.value) / (self._ratings_count.value + 1))

    @property
    def release_year(self) -> ReleaseYear:
        return self._release_year

    @classmethod
    def create(
        cls,
        id: BookId,
        title: Title,
        author: Author,
        rating: Rating,
        ratings_count: RatingsCount,
        release_year: ReleaseYear,
    ) -> Book:
        return cls(
            id=id,
            title=title,
            author=author,
            rating=rating,
            ratings_count=ratings_count,
            release_year=release_year,
        )

    def __str__(self) -> str:
        return f"Книга {self.title} автора {self.author}"

    # fill with methods
