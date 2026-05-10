class DomainError(Exception):
    """Базовый класс для всех ошибок доменной логики."""
    status_code: int = 400

    def __init__(self, message: str = "Domain error occurred"):
        super().__init__(message)


class UserAlreadyExistsError(DomainError):
    """
    Поднимается, когда пользователь с такими уникальными
    атрибутами уже существует.
    """

    status_code: int = 409


class InvalidRegistrationDataError(DomainError):
    """Поднимается, когда данные для регистрации некорректны."""

    status_code: int = 400


class InvalidLoginDataError(DomainError):
    """Поднимается, когда данные для входа некорректны."""

    status_code: int = 401


class UserNotFoundError(DomainError):
    """Поднимается, когда пользователь не найден."""

    status_code: int = 404


class PermissionDeniedError(DomainError):
    """Raised when a user is not allowed to perform an action."""

    status_code: int = 403


class InvalidBookDataError(DomainError):
    """Поднимается, когда данные для создания книги некорректны."""

    status_code: int = 400


class BookAlreadyExistsError(DomainError):
    """Поднимается, когда книга с такими уникальными атрибутами уже существует."""

    status_code: int = 409


class BookNotFoundError(DomainError):
    """Поднимается, когда книга не найдена."""

    status_code: int = 404


class InvalidReviewDataError(DomainError):
    """Поднимается, когда данные для создания отзыва некорректны."""

    status_code: int = 400


class ReviewAlreadyExistsError(DomainError):
    """Поднимается, когда отзыв с такими уникальными атрибутами уже существует."""

    status_code: int = 409


class ReviewNotFoundError(DomainError):
    """Поднимается, когда отзыв не найден."""

    status_code: int = 404


class InvalidUserDataError(DomainError):
    """Поднимается, когда данные пользователя некорректны."""

    status_code: int = 400


class InvalidUserListDataError(DomainError):
    """Поднимается, когда данные для создания списка некорректны."""

    status_code: int = 400


class UserListAlreadyExistsError(DomainError):
    """Поднимается, когда список с такими уникальными атрибутами уже существует."""

    status_code: int = 409


class UserListNotFoundError(DomainError):
    """Raised when a user book list is not found."""

    status_code: int = 404


class BookAlreadyInUserListError(DomainError):
    """Raised when a book is already present in a user book list."""

    status_code: int = 409


class BookNotInUserListError(DomainError):
    """Raised when a book is not present in a user book list."""

    status_code: int = 404


class InvalidLLMRequestError(DomainError):
    """Поднимается, когда данные для LLM-запроса некорректны."""

    status_code: int = 400
