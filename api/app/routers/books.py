from fastapi import APIRouter, Depends

from api.app.dependencies.container import get_create_book, get_get_book_by_id
from thelibrary.use_cases.book import CreateBook, CreateBookCommand, GetBookById, GetBookByIdCommand
from api.app.schemas.book import BookResponse, to_book_response

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/")
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

@router.get("/", response_model=BookResponse)
def get_book(
    id: str,
    use_case: GetBookById = Depends(get_get_book_by_id),
):
    command = GetBookByIdCommand(
        id=id,
    )
    book = use_case.execute(command)

    return to_book_response(book)
