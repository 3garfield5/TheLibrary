from pydantic import BaseModel


class UserListCreateRequest(BaseModel):
    title: str
    description: str = ""
    is_private: bool = False
    user_id: str


class UserListResponse(BaseModel):
    id: str
    title: str
    description: str
    is_private: bool
    user_id: str
    book_ids: list[str]


def to_user_list_response(user_list) -> UserListResponse:
    return UserListResponse(
        id=user_list.id.value,
        title=user_list.title.value,
        description=user_list.description.value,
        is_private=user_list.is_private.value,
        user_id=user_list.user_id.value,
        book_ids=[book_id.value for book_id in user_list.books],
    )
