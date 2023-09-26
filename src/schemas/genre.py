from pydantic import BaseModel, ConfigDict


class GenreBase(BaseModel):
    name: str = "Fiction"


class GenreRead(GenreBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class GenreCreate(GenreBase):
    pass


class GenreUpdate(GenreBase):
    pass

