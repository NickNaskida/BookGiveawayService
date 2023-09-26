from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    full_name: str = "Robert C. Martin"


class AuthorRead(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    pass

