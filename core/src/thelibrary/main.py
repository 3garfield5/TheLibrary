from domain.entities import Book, Review, User
from domain.repositories import BookRepository, UserRepository, ReviewRepository
from use_cases.book import CreateBook, CreateBookCommand
from use_cases.user import GetUserById, GetUserByIdCommand, RegisterUser, RegisterUserCommand
from use_cases.review import CreateReview, CreateReviewCommand

if __name__ == "__main__":
    # Пример регистрации пользователя, создания книги и отзыва
    user_repository = UserRepository()
    book_repository = BookRepository()
    review_repository = ReviewRepository()

    register_user = RegisterUser(user_repository)
    create_book = CreateBook(book_repository)
    get_user_by_id = GetUserById(user_repository)
    create_review = CreateReview(review_repository)

    # Регистрируем пользователя
    user_command = RegisterUserCommand(
        username="john_doe",
        email="john.doe@example.com",
        password_hash="hashed_password"
    )
    user_id = register_user.execute(user_command)
    print(f"Пользователь зарегистрирован с ID: {user_id.value}")

    # Создаем книгу
    book_command = CreateBookCommand(
        title="The Great Gatsby",
        author="F. Scott Fitzgerald",
        rating=4.5,
        ratings_count=1000,
        publication_year=1925
    )
    book_id = create_book.execute(book_command)
    print(f"Книга создана с ID: {book_id.value}")

    # Получаем пользователя по ID
    get_user_command = GetUserByIdCommand(id=user_id.value)
    user = get_user_by_id.execute(get_user_command)
    print(f"Получен пользователь: {user.username.value} с email: {user.email.value}")

    # Создаем отзыв
    review_command = CreateReviewCommand(
        user_id=user_id.value,
        book_id=book_id.value,
        rating=5,
        comment="Отличная книга!"
    )
    review_id = create_review.execute(review_command)
    print(f"Отзыв создан с ID: {review_id.value}")