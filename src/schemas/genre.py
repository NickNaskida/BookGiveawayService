from pydantic import BaseModel, ConfigDict


class GenreBase(BaseModel):
    name: str = "Self-help"


class GenreRead(GenreBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class GenreCreate(GenreBase):
    pass


class GenreUpdate(GenreBase):
    pass

