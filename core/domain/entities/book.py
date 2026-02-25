from ..value_objects.book_id import BookId
from ..value_objects.title import Title
from ..value_objects.author import Author
from ..value_objects.rating import Rating
from ..value_objects.ratings_count import RatingsCount
from ..value_objects.release_year import ReleaseYear

def _require_type(value, expected_type, name):
    if not isinstance(value, expected_type):
        raise TypeError(f'{name} must be {expected_type.__name__}')

class Book:
    def __init__(self, id: BookId, title: Title, author: Author, rating: Rating, ratings_count: RatingsCount, release_year: ReleaseYear):
        _require_type(id, BookId, "book_id")
        _require_type(title, Title, "title")
        _require_type(author, Author, "author")
        _require_type(rating, Rating, "rating")
        _require_type(ratings_count, RatingsCount, "ratings_count")
        _require_type(release_year, ReleaseYear, "release_year")

        self._id = id
        self._title = title
        self._author = author
        self._rating = rating
        self._ratings_count = ratings_count
        self._release_year = release_year

    @property
    def id(self):
        return self._id
    
    @property
    def title(self):
        return self._title
    
    @property
    def author(self):
        return self._author
    
    @property
    def rating(self):
        return self._rating
    
    @property
    def ratings_count(self):
        return self._ratings_count
    
    @property
    def release_year(self):
        return self._release_year

    def __str__(self):
        return f'Книга {self.title} автора {self.author}. Рейтинг: {self.rating}, год выпуска: {self.release_year}'

    # fill with methods