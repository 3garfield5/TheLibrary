from thelibrary.use_cases.user import RegisterUser, LoginUser, GetUserById
from thelibrary.use_cases.book import CreateBook
from infrastructure.repositories.in_memory import (
    InMemoryUserRepository,
    InMemoryBookRepository,
)

repo = InMemoryUserRepository()

book_repo = InMemoryBookRepository()


def get_register_user() -> RegisterUser:
    return RegisterUser(repo)


def get_login_user() -> LoginUser:
    return LoginUser(repo)


def get_get_user_by_id() -> GetUserById:
    return GetUserById(repo)


def get_create_book() -> CreateBook:
    return CreateBook(book_repo)
