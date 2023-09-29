from typing import List

from pydantic import BaseModel, ConfigDict

from src.models.book import BookCondition
from src.schemas.author import AuthorRead
from src.schemas.genre import GenreRead
from src.schemas.location import LocationRead


class BookBase(BaseModel):
    name: str = "Atomic Habits"
    description: str = "Tiny Changes, Remarkable Results"
    condition: BookCondition = BookCondition.NEW
    page_count: int = 320


class BookRead(BookBase):
    id: int
    author: AuthorRead
    genre: GenreRead
    locations: List[LocationRead]

    model_config = ConfigDict(from_attributes=True)


class BookCreate(BookBase):
    author_id: int = 1
    genre_id: int = 1


class BookUpdate(BookBase):
    author_id: int = 1
    genre_id: int = 1


class BookLocationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BookLocationRead(BookLocationBase):
    book: BookRead
    location: LocationRead


class BookLocationCreate(BookLocationBase):
    book_id: int
    location_id: int


class BookLocationUpdate(BookLocationBase):
    book_id: int
    location_id: int
