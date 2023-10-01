from typing import List
from fastapi import APIRouter, HTTPException, Response, Depends

from src import crud
from src.models import User
from src.models.book import BookRequestStatus
from src.api.deps import current_active_superuser, current_active_user
from src.schemas.book import BookRequestRead, BookRequestCreate, BookRequestUpdate


router = APIRouter()


@router.get("/{book_id}")
async def get_book_requests(
    book_id: int,
    user: User = Depends(current_active_user)
) -> List[BookRequestRead]:
    """
    Get all book request.

    Required role:
    - Verified user
    - Be the owner of the book

    :param book_id: Book id.
    :param user: Current user.
    :return: List of book request objects.
    """
    # Check if book exists
    book = await crud.book.get(book_id)
    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    # Check if user is the owner of the book
    if book.owner_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not the owner of the book"
        )

    book_requests = await crud.request.get_by_book(book_id=book_id)
    return book_requests


@router.post("/{book_id}", status_code=201)
async def create_book_request(
    book_id: int,
    user: User = Depends(current_active_user)
) -> BookRequestRead:
    """
    Create new book request.

    Required role:
    - Verified user

    :param book_id: Requested book id.
    :param user: Current user.
    :return: Book request object.
    """
    # Check if book exists
    book = await crud.book.get(book_id)
    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    # Check if user is the owner of the book
    if book.owner_id == user.id:
        raise HTTPException(
            status_code=403,
            detail="You are the owner of the book. You cannot request your own book."
        )

    # Check if request already exists
    existing_request = await crud.request.get_by_book_and_requester(
        book_id=book_id,
        requester_id=user.id
    )
    if existing_request:
        raise HTTPException(
            status_code=400,
            detail="Request already exists"
        )

    book_request = BookRequestCreate(
        book_id=book_id,
        requester_id=user.id,
        status=BookRequestStatus.PENDING
    )

    book_request = await crud.request.create(obj_in=book_request)
    return book_request


@router.patch("/{request_id}")
async def accept_book_request(
    request_id: int,
    user: User = Depends(current_active_user)
) -> BookRequestRead:
    """
    Accept book request for single user and reject all other requests.

    Required role:
    - Verified user
    - Be the owner of the book

    :param request_id: Book request id.
    :param user: Current user.
    :return: Book request object.
    """
    # Check if request exists
    book_request = await crud.request.get(request_id)
    if not book_request:
        raise HTTPException(
            status_code=404,
            detail="Book request not found"
        )

    # TODO: Check if request was already accepted

    # Check if user is the owner of the book
    book = await crud.book.get(book_request.book_id)
    if book.owner_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not the owner of the book"
        )

    # Accept request
    book_request_new = BookRequestUpdate(
        book_id=book_request.book_id,
        requester_id=book_request.requester_id,
        status=BookRequestStatus.ACCEPTED
    )
    book_request = await crud.request.update(
        obj_current=book_request,
        obj_new=book_request_new,
    )

    # Reject all other requests
    await crud.request.reject_all_requests_for_book(
        book_id=book_request.book_id
    )

    return book_request

