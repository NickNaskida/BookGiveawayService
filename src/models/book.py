from enum import Enum

from sqlalchemy import Column, Integer, String, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from fastapi_users_db_sqlalchemy.generics import GUID

from src.models.base import PkBase


class BookCondition(Enum):
    NEW = 'new'
    USED = 'used'
    DAMAGED = 'damaged'


class BookRequestStatus(Enum):
    IDLE = 'idle'
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'


class Book(PkBase):
    """Book model."""
    __tablename__ = 'books'

    name = Column(String(100))
    description = Column(String(500))
    condition = Column(SQLEnum(BookCondition))
    page_count = Column(Integer)
    owner_id = Column(GUID, ForeignKey('user.id'))
    owner = relationship('User', lazy='selectin')
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship('Author', back_populates='books', lazy='selectin')
    genre_id = Column(Integer, ForeignKey('genres.id'))
    genre = relationship('Genre', back_populates='books', lazy='selectin')
    locations = relationship('BookLocation', back_populates='book', lazy='selectin')


class BookRequest(PkBase):
    """Book request model."""
    __tablename__ = 'book_requests'

    book_id = Column(Integer, ForeignKey('books.id'))
    book = relationship('Book', lazy='selectin')
    requester_id = Column(GUID, ForeignKey('user.id'))
    requester = relationship('User', lazy='selectin')
    status = Column(SQLEnum(BookRequestStatus))
