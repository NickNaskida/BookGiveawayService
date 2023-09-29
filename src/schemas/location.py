from pydantic import BaseModel, ConfigDict


class LocationBase(BaseModel):
    name: str = "Jen's Bookshop"
    address: str = "123 Main St"


class LocationRead(LocationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class LocationCreate(LocationBase):
    pass


class LocationUpdate(LocationBase):
    pass
