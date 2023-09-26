from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.models.base import PkBase


class Genre(PkBase):
    """Book genre model."""
    __tablename__ = 'genres'

    name = Column(String(100), unique=True)
    books = relationship('Book', back_populates='genre')

    def __repr__(self):
        return f'<Genre {self.name}>'
