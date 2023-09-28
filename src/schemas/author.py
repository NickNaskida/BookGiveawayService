from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    full_name: str = "James Clear"


class AuthorRead(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    pass

