from fastapi import APIRouter, Depends

from api.app.dependencies.container import get_create_book
from thelibrary.use_cases.book import CreateBook, CreateBookCommand

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/book")
def add_book(
    title: str,
    author: str,
    release_year: int,
    use_case: CreateBook = Depends(get_create_book),
):
    command = CreateBookCommand(
        title=title,
        author=author,
        release_year=release_year,
    )
    book_id = use_case.execute(command)

    return {"book_id": str(book_id)}
