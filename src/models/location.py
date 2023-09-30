from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.models.base import PkBase


class BookLocation(PkBase):
    """Book location model."""
    __tablename__ = 'book_locations'

    address = Column(String(70))
    book_id = Column(Integer, ForeignKey('books.id'))
    book = relationship('Book', back_populates='locations', lazy='selectin')
