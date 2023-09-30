import uuid
from typing import List

from pydantic import BaseModel, ConfigDict, Field

from src.models.book import BookCondition
from src.schemas.author import AuthorRead
from src.schemas.genre import GenreRead
from src.schemas.user import UserRead


class BookBase(BaseModel):
    name: str = "Atomic Habits"
    description: str = "Tiny Changes, Remarkable Results"
    condition: BookCondition = BookCondition.NEW
    page_count: int = 320


class BookLocationBase(BaseModel):
    address: str

    model_config = ConfigDict(from_attributes=True)


class BookRead(BookBase):
    id: int
    author: AuthorRead
    genre: GenreRead
    locations: List[BookLocationBase]
    owner_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class BookCreate(BookBase):
    author_id: int = 1
    genre_id: int = 1
    owner_id: uuid.UUID


class BookUpdate(BookBase):
    author_id: int = 1
    genre_id: int = 1


class BookLocationRead(BookLocationBase):
    book: BookRead


class BookLocationCreate(BookLocationBase):
    book_id: int


class BookLocationUpdate(BookLocationBase):
    book_id: int
