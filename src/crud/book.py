from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.crud.base import CRUDBase
from src.models import Book, Author, Genre
from src.schemas.book import BookCreate, BookUpdate


class CRUDBook(CRUDBase[Book, BookCreate, BookUpdate]):
    async def filter_by_params(
        self,
        genre: str,
        author: str,
        condition: str,
        db_session: AsyncSession | None = None
    ) -> List[Book]:
        """
        Get all books filtered by params.

        :param genre: Genre name.
        :param author: Author name.
        :param condition: Book condition.
        :param db_session: Database session.
        :return: List of book objects.
        """
        db_session = db_session or self.get_db().session

        query = select(Book)

        if genre:
            query = query.join(Genre).where(Genre.name == genre)
        if author:
            query = query.join(Author).where(Author.full_name == author)
        if condition:
            query = query.where(Book.condition == condition)

        response = await db_session.execute(query)

        return response.scalars().all()


book = CRUDBook(Book)
