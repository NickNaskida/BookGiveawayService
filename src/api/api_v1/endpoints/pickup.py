from fastapi import APIRouter, HTTPException, Response, Depends

from src import crud
from src.models import User
from src.api.deps import current_active_user
from src.schemas.book import BookLocationRead, BookLocationCreate

router = APIRouter()


@router.post("/", status_code=201)
async def add_pickup_location_for_book(
    pickup_location_new: BookLocationCreate,
    current_user: User = Depends(current_active_user)
) -> BookLocationRead:
    """
    Add a pickup location for a book.

    Roles required:
    - Be a verified user
    - Be the owner of the book

    :param pickup_location_new: Pickup location to add.
    :param current_user: Superuser user object.
    :return: The pickup location.
    """
    # Check if book exists
    book = await crud.book.get(_id=pickup_location_new.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    pickup_location = await crud.pickup.create(obj_in=pickup_location_new)
    return pickup_location


# TODO: Add EDIT & DELETE endpoints
