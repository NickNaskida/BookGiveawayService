from src.crud.base import CRUDBase
from src.models.genre import Genre
from src.schemas.genre import GenreCreate, GenreUpdate


class CRUDGenre(CRUDBase[Genre, GenreCreate, GenreUpdate]):
    pass


genre = CRUDGenre(Genre)
