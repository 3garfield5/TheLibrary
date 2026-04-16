from __future__ import annotations

from infrastructure.llm.contracts import build_llm_repository
from thelibrary.use_cases.book import CreateBook
from thelibrary.use_cases.llm import ChatWithAssistant, RecommendBooks
from thelibrary.use_cases.user import GetUserById, LoginUser, RegisterUser

from infrastructure.repositories.in_memory import InMemoryBookRepository, InMemoryUserRepository

repo = InMemoryUserRepository()
book_repo = InMemoryBookRepository()

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
    return CreateBook(book_repo)


def get_recommend_books() -> RecommendBooks | None:
    return _recommend_books


def get_chat_with_assistant() -> ChatWithAssistant | None:
    return _chat_with_assistant


def get_llm_initialization_error() -> str | None:
    return _llm_initialization_error
