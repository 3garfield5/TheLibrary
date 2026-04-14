from fastapi import APIRouter, Depends

from api.app.dependencies.container import (
    get_register_user,
    get_login_user,
    get_get_user_by_id,
)
from thelibrary.use_cases.user import (
    RegisterUser,
    RegisterUserCommand,
    LoginUser,
    LoginUserCommand,
    GetUserById,
    GetUserByIdCommand,
)
from api.app.schemas.user import UserResponse, to_user_response

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register")
def register_user(
    username: str,
    email: str,
    password: str,
    use_case: RegisterUser = Depends(get_register_user),
):
    command = RegisterUserCommand(
        username=username,
        email=email,
        password_hash=password,  # позже заменишь на hasher
    )
    user_id = use_case.execute(command)

    return {"user_id": str(user_id)}


@router.post("/login")
def login_user(
    email: str,
    password: str,
    use_case: LoginUser = Depends(get_login_user),
):
    command = LoginUserCommand(
        email=email,
        password_hash=password,  # позже заменишь на hasher
    )
    user_id = use_case.execute(command)

    return {"user_id": str(user_id)}


@router.get("/me", response_model=UserResponse)
def get_user_by_id(
    user_id: str,
    use_case: GetUserById = Depends(get_get_user_by_id),
):
    command = GetUserByIdCommand(id=user_id)
    user = use_case.execute(command)

    return to_user_response(user)
