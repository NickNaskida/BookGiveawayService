from enum import Enum

from sqlalchemy import Column, Integer, String, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship

from src.models.base import PkBase


class BookCondition(Enum):
    NEW = 'new'
    USED = 'used'
    DAMAGED = 'damaged'


class Book(PkBase):
    """Book model."""
    __tablename__ = 'books'

    title = Column(String(100))
    description = Column(String(500))
    condition = Column(SQLEnum(BookCondition))
    page_count = Column(Integer)
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship('Author', back_populates='books')
    genre_id = Column(Integer, ForeignKey('genres.id'))
    genre = relationship('Genre', back_populates='books')



