from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.models.base import PkBase


class Location(PkBase):
    """Location model."""
    __tablename__ = 'locations'

    name = Column(String(50), unique=True)
    address = Column(String(70))
    books = relationship('BookLocation', back_populates='location', lazy='selectin')


class BookLocation(PkBase):
    """Book location model."""
    __tablename__ = 'book_locations'

    book_id = Column(Integer, ForeignKey('books.id'))
    book = relationship('Book', back_populates='locations', lazy='selectin')
    location_id = Column(Integer, ForeignKey('locations.id'))
    location = relationship('Location', back_populates='books', lazy='selectin')
