from fastapi import APIRouter, Depends, status

from api.app.dependencies.container import (
    get_create_book,
    get_delete_book,
    get_get_book_by_id,
    get_update_book,
)
from api.app.schemas.book import BookResponse, to_book_response
from thelibrary.use_cases.book import (
    CreateBook,
    CreateBookCommand,
    DeleteBook,
    DeleteBookCommand,
    GetBookById,
    GetBookByIdCommand,
    UpdateBook,
    UpdateBookCommand,
)

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_book(
    title: str,
    author: str,
    release_year: int,
    admin_user_id: str,
    use_case: CreateBook = Depends(get_create_book),
):
    command = CreateBookCommand(
        title=title,
        author=author,
        release_year=release_year,
        admin_user_id=admin_user_id,
    )
    book_id = use_case.execute(command)

    return {"book_id": book_id.value}


@router.get("/", response_model=BookResponse)
def get_book(
    id: str,
    use_case: GetBookById = Depends(get_get_book_by_id),
):
    book = use_case.execute(GetBookByIdCommand(id=id))

    return to_book_response(book)


@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: str,
    title: str,
    author: str,
    release_year: int,
    admin_user_id: str,
    use_case: UpdateBook = Depends(get_update_book),
):
    book = use_case.execute(
        UpdateBookCommand(
            id=book_id,
            title=title,
            author=author,
            release_year=release_year,
            admin_user_id=admin_user_id,
        )
    )

    return to_book_response(book)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: str,
    admin_user_id: str,
    use_case: DeleteBook = Depends(get_delete_book),
):
    use_case.execute(DeleteBookCommand(id=book_id, admin_user_id=admin_user_id))
