from domain.entities.book import Book
from domain.value_objects.book_id import BookId
from domain.value_objects.title import Title
from domain.value_objects.author import Author
from domain.value_objects.rating import Rating
from domain.value_objects.release_year import ReleaseYear

if __name__ == "__main__":
    book = Book(id=BookId(1), title=Title("1984"), author=Author("Джордж Оруэлл"), rating=Rating(4.99), release_year=ReleaseYear(1975))
    print(book)
    print(book)