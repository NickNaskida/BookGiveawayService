from src.crud.base import CRUDBase
from src.models.location import BookLocation
from src.schemas.book import BookLocationCreate, BookLocationUpdate


class CRUDPickup(CRUDBase[BookLocation, BookLocationCreate, BookLocationUpdate]):
    pass


pickup = CRUDPickup(BookLocation)
