from src.crud.base import CRUDBase
from src.models.location import Location
from src.schemas.location import LocationCreate, LocationUpdate


class CRUDLocation(CRUDBase[Location, LocationCreate, LocationUpdate]):
    pass


location = CRUDLocation(Location)
