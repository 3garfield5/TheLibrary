from thelibrary.use_cases.user import RegisterUser, LoginUser, GetUserById
from thelibrary.use_cases.book import CreateBook, GetBookById
from thelibrary.use_cases.review import CreateReview, GetReviewById
from infrastructure.repositories.in_memory import (
    InMemoryUserRepository,
    InMemoryBookRepository,
    InMemoryReviewRepository
)

repo = InMemoryUserRepository()

book_repo = InMemoryBookRepository()

review_repo = InMemoryReviewRepository()


def get_register_user() -> RegisterUser:
    return RegisterUser(repo)


def get_login_user() -> LoginUser:
    return LoginUser(repo)


def get_get_user_by_id() -> GetUserById:
    return GetUserById(repo)


def get_create_book() -> CreateBook:
    return CreateBook(book_repo)

def get_get_book_by_id() -> GetBookById:
    return GetBookById(book_repo)

def get_create_review() -> CreateReview:
    return CreateReview(review_repo, book_repo)

def get_get_review_by_id() -> GetReviewById:
    return GetReviewById(review_repo)
