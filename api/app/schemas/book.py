from pydantic import BaseModel


class BookResponse(BaseModel):
    id: str
    title: str
    author: str
    rating: float
    ratings_count: int
    release_year: int


def to_book_response(book) -> BookResponse:
    return BookResponse(
        id=str(book.id.value),
        title=book.title.value,
        author=book.author.value,
        rating=book.rating.value,
        ratings_count=book.ratings_count.value,
        release_year=book.release_year.value
    )
