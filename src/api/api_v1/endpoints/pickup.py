from typing import List
from fastapi import APIRouter, HTTPException, Response, Depends

from src import crud
from src.models import User
from src.api.deps import current_active_superuser
from src.schemas.location import LocationRead
from src.schemas.book import BookLocationRead, BookLocationCreate

router = APIRouter()


@router.get("/")
async def get_all_pickup_locations() -> List[LocationRead]:
    """
    Get all pickup locations.

    :return: List of pickup locations.
    """
    pickup_locations = await crud.location.get_multi()
    return pickup_locations


@router.post("/")
async def add_pickup_location_for_book(
    pickup_location_new: BookLocationCreate,
    current_user: User = Depends(current_active_superuser)
) -> BookLocationRead:
    """
    Add a pickup location for a book.

    :param pickup_location_new: Pickup location to add.
    :param current_user: Superuser user object.
    :return: The pickup location.
    """
    # Check if book exists
    book = await crud.book.get(_id=pickup_location_new.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Check if location exists
    location = await crud.location.get(_id=pickup_location_new.location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    pickup_location = await crud.pickup.create(obj_in=pickup_location_new)
    return pickup_location


# TODO: EDIT & DELETE endpoints
