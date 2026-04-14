from pydantic import BaseModel


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    is_admin: bool


def to_user_response(user) -> UserResponse:
    return UserResponse(
        id=str(user.id.value),
        username=user.username.value,
        email=user.email.value,
        is_admin=user.is_admin.value,  # если bool
    )
