from __future__ import annotations

from infrastructure.llm.contracts import build_llm_repository
from thelibrary.use_cases.book import CreateBook, DeleteBook, GetBookById, UpdateBook
from thelibrary.use_cases.llm import ChatWithAssistant, RecommendBooks
from thelibrary.use_cases.review import CreateReview, DeleteReview, GetReviewById
from thelibrary.use_cases.user import GetUserById, LoginUser, RegisterUser
from thelibrary.use_cases.user_list import (
    AddBookToUserList,
    CreateUserList,
    DeleteUserList,
    GetUserListById,
    GetUserListsByUserId,
    RemoveBookFromUserList,
)

from infrastructure.repositories.postgres import (
    PostgresBookRepository,
    PostgresReviewRepository,
    PostgresUserRepository,
    PostgresUserListRepository,
    init_postgres_schema,
)


def _build_repositories():
    init_postgres_schema()
    return (
        PostgresUserRepository(),
        PostgresBookRepository(),
        PostgresReviewRepository(),
        PostgresUserListRepository(),
    )


repo, book_repo, review_repo, user_list_repo = _build_repositories()

_llm_initialization_error: str | None = None
_recommend_books: RecommendBooks | None = None
_chat_with_assistant: ChatWithAssistant | None = None

try:
    llm_repository = build_llm_repository()
    _recommend_books = RecommendBooks(llm_repository)
    _chat_with_assistant = ChatWithAssistant(llm_repository)
except Exception as exc:
    _llm_initialization_error = str(exc)


def get_register_user() -> RegisterUser:
    return RegisterUser(repo)


def get_login_user() -> LoginUser:
    return LoginUser(repo)


def get_get_user_by_id() -> GetUserById:
    return GetUserById(repo)


def get_create_book() -> CreateBook:
    return CreateBook(book_repo, repo)


def get_get_book_by_id() -> GetBookById:
    return GetBookById(book_repo)


def get_update_book() -> UpdateBook:
    return UpdateBook(book_repo, repo)


def get_delete_book() -> DeleteBook:
    return DeleteBook(book_repo, repo)


def get_create_review() -> CreateReview:
    return CreateReview(review_repo, book_repo, repo)


def get_get_review_by_id() -> GetReviewById:
    return GetReviewById(review_repo)


def get_delete_review() -> DeleteReview:
    return DeleteReview(review_repo, book_repo, repo)


def get_create_user_list() -> CreateUserList:
    return CreateUserList(user_list_repo, repo)


def get_get_user_list_by_id() -> GetUserListById:
    return GetUserListById(user_list_repo)


def get_get_user_lists_by_user_id() -> GetUserListsByUserId:
    return GetUserListsByUserId(user_list_repo, repo)


def get_delete_user_list() -> DeleteUserList:
    return DeleteUserList(user_list_repo)


def get_add_book_to_user_list() -> AddBookToUserList:
    return AddBookToUserList(user_list_repo, book_repo)


def get_remove_book_from_user_list() -> RemoveBookFromUserList:
    return RemoveBookFromUserList(user_list_repo)


def get_recommend_books() -> RecommendBooks | None:
    return _recommend_books


def get_chat_with_assistant() -> ChatWithAssistant | None:
    return _chat_with_assistant


def get_llm_initialization_error() -> str | None:
    return _llm_initialization_error
