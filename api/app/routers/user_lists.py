from fastapi import APIRouter, Depends, status

from api.app.dependencies.container import (
    get_add_book_to_user_list,
    get_create_user_list,
    get_delete_user_list,
    get_get_user_list_by_id,
    get_get_user_lists_by_user_id,
    get_remove_book_from_user_list,
)
from api.app.schemas.user_list import (
    UserListCreateRequest,
    UserListResponse,
    to_user_list_response,
)
from thelibrary.use_cases.user_list import (
    AddBookToUserList,
    AddBookToUserListCommand,
    CreateUserList,
    CreateUserListCommand,
    DeleteUserList,
    DeleteUserListCommand,
    GetUserListById,
    GetUserListByIdCommand,
    GetUserListsByUserId,
    GetUserListsByUserIdCommand,
    RemoveBookFromUserList,
    RemoveBookFromUserListCommand,
)

router = APIRouter(prefix="/user-lists", tags=["user-lists"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user_list(
    payload: UserListCreateRequest,
    use_case: CreateUserList = Depends(get_create_user_list),
):
    command = CreateUserListCommand(
        title=payload.title,
        description=payload.description,
        is_private=payload.is_private,
        user_id=payload.user_id,
    )
    user_list_id = use_case.execute(command)

    return {"user_list_id": user_list_id.value}


@router.get("/users/{user_id}", response_model=list[UserListResponse])
def get_user_lists_by_user(
    user_id: str,
    use_case: GetUserListsByUserId = Depends(get_get_user_lists_by_user_id),
):
    user_lists = use_case.execute(GetUserListsByUserIdCommand(user_id=user_id))

    return [to_user_list_response(user_list) for user_list in user_lists]


@router.get("/{user_list_id}", response_model=UserListResponse)
def get_user_list(
    user_list_id: str,
    use_case: GetUserListById = Depends(get_get_user_list_by_id),
):
    user_list = use_case.execute(GetUserListByIdCommand(id=user_list_id))

    return to_user_list_response(user_list)


@router.delete("/{user_list_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_list(
    user_list_id: str,
    use_case: DeleteUserList = Depends(get_delete_user_list),
):
    use_case.execute(DeleteUserListCommand(id=user_list_id))


@router.post("/{user_list_id}/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def add_book_to_user_list(
    user_list_id: str,
    book_id: str,
    use_case: AddBookToUserList = Depends(get_add_book_to_user_list),
):
    use_case.execute(
        AddBookToUserListCommand(user_list_id=user_list_id, book_id=book_id)
    )


@router.delete("/{user_list_id}/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_book_from_user_list(
    user_list_id: str,
    book_id: str,
    use_case: RemoveBookFromUserList = Depends(get_remove_book_from_user_list),
):
    use_case.execute(
        RemoveBookFromUserListCommand(user_list_id=user_list_id, book_id=book_id)
    )
