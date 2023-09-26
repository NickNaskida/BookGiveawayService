from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.models.base import PkBase


class Author(PkBase):
    """Author model."""
    __tablename__ = 'authors'

    full_name = Column(String(100), unique=True)
    books = relationship('Book', back_populates='author')

    def __repr__(self):
        return f'<Author {self.full_name}>'
