import uuid
from typing import List

from sqlalchemy import select

from src.crud.base import CRUDBase
from src.models.book import BookRequest, BookRequestStatus
from src.schemas.book import BookRequestCreate, BookRequestUpdate


class CRUDBookRequest(CRUDBase[BookRequest, BookRequestCreate, BookRequestUpdate]):
    async def get_by_book(self, book_id: int) -> List[BookRequest]:
        """
        Get book requests by book id.

        :param book_id: Book id
        :return:
        """
        db_session = self.get_db().session

        query = select(BookRequest).where(BookRequest.book_id == book_id)
        result = await db_session.execute(query)
        return result.scalars().all()

    async def get_by_book_and_requester(
        self,
        book_id: int,
        requester_id: uuid.UUID
    ) -> BookRequest:
        """
        Get book request by book id and requester id.

        :param book_id: Book id
        :param requester_id: Requester user id
        :return:
        """
        db_session = self.get_db().session

        query = select(BookRequest).where(
            (BookRequest.book_id == book_id) &
            (BookRequest.requester_id == requester_id)
        )
        result = await db_session.execute(query)
        return result.scalar_one_or_none()

    async def reject_all_requests_for_book(self, book_id: int) -> None:
        """
        Reject all book requests except the one with the given id.

        :param book_id: Book id
        :return: None
        """
        db_session = self.get_db().session

        query = select(BookRequest).where(
            (BookRequest.book_id == book_id) &
            (BookRequest.status != BookRequestStatus.ACCEPTED)
        )
        result = await db_session.execute(query)
        requests = result.scalars().all()

        for request in requests:
            request.status = BookRequestStatus.REJECTED

        await db_session.commit()


request = CRUDBookRequest(BookRequest)
