from pydantic import BaseModel, ConfigDict

from src.models.book import BookCondition
from src.schemas.author import AuthorRead
from src.schemas.genre import GenreRead


class BookBase(BaseModel):
    name: str = "Atomic Habits"
    description: str = "Tiny Changes, Remarkable Results"
    condition: BookCondition = BookCondition.NEW
    page_count: int = 320


class BookRead(BookBase):
    id: int
    author: AuthorRead
    genre: GenreRead

    model_config = ConfigDict(from_attributes=True)


class BookCreate(BookBase):
    author_id: int = 1
    genre_id: int = 1


class BookUpdate(BookBase):
    author_id: int = 1
    genre_id: int = 1
