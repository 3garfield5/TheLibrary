class UserAlreadyExistsError(Exception):
    """
    Поднимается, когда пользователь с такими уникальными
    атрибутами уже существует.
    """

    pass


class InvalidRegistrationDataError(Exception):
    """Поднимается, когда данные для регистрации некорректны."""

    pass


class InvalidLoginDataError(Exception):
    """Поднимается, когда данные для входа некорректны."""

    pass


class UserNotFoundError(Exception):
    """Поднимается, когда пользователь не найден."""

    pass


class InvalidBookDataError(Exception):
    """Поднимается, когда данные для создания книги некорректны."""

    pass


class BookAlreadyExistsError(Exception):
    """Поднимается, когда книга с такими уникальными атрибутами уже существует."""

    pass


class BookNotFoundError(Exception):
    """Поднимается, когда книга не найдена."""

    pass


class InvalidReviewDataError(Exception):
    """Поднимается, когда данные для создания отзыва некорректны."""

    pass


class ReviewAlreadyExistsError(Exception):
    """Поднимается, когда отзыв с такими уникальными атрибутами уже существует."""

    pass


class ReviewNotFoundError(Exception):
    """Поднимается, когда отзыв не найден."""

    pass


class InvalidUserDataError(Exception):
    """Поднимается, когда данные для создания пользователя некорректны."""

    pass
