from src.crud.base import CRUDBase
from src.models.author import Author
from src.schemas.author import AuthorCreate, AuthorUpdate


class CRUDAuthor(CRUDBase[Author, AuthorCreate, AuthorUpdate]):
    pass


author = CRUDAuthor(Author)
