from typing import List
from fastapi import APIRouter, HTTPException, Response, Depends

from src import crud
from src.models import User
from src.api.deps import current_active_superuser
from src.schemas.genre import GenreRead, GenreCreate, GenreUpdate


router = APIRouter()


@router.get("/")
async def get_genres() -> List[GenreRead]:
    """
    Get all genres.

    :return: List of genre objects.
    """
    genres = await crud.genre.get_multi()
    return genres


@router.get(
    "/{genre_id}",
    responses={
        404: {"description": "Genre not found"},
        409: {"description": "Genre already exists"},
    }
)
async def get_genre_by_id(genre_id: int) -> GenreRead:
    """
    Get genre by id.

    :param genre_id: Genre id.
    :return: Genre object.
    """
    genre = await crud.genre.get(_id=genre_id)

    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    return genre


@router.post("/", responses={409: {"description": "Genre already exists"}}, status_code=201)
async def create_genre(
    genre_new: GenreCreate,
    user: User = Depends(current_active_superuser)
) -> GenreRead:
    """
    Create new genre.

    Required role:
    - Superuser

    :param genre_new: Genre object.
    :param user: Superuser user object.
    :return: Created genre object.
    """
    genre = await crud.genre.create(obj_in=genre_new)
    return genre


@router.put(
    "/{genre_id}",
    responses={
        404: {"description": "Genre not found"},
        409: {"description": "Genre already exists"},
    }
)
async def update_genre(
    genre_id: int,
    genre_new: GenreUpdate,
    user: User = Depends(current_active_superuser)
) -> GenreRead:
    """
    Update genre by id.

    Required role:
    - Superuser

    :param genre_id: Genre id.
    :param genre_new: New genre object.
    :paSuperuser user object.
    :return: Updated genre object.
    """
    genre = await crud.genre.get(_id=genre_id)

    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    genre = await crud.genre.update(obj_current=genre, obj_new=genre_new)
    return genre


@router.delete("/{genre_id}", responses={404: {"description": "Genre not found"}})
async def delete_genre(
    genre_id: int,
    user: User = Depends(current_active_superuser)
) -> Response:
    """
    Delete genre by id.

    Required role:
    - Superuser

    :param genre_id: Genre id.
    :param user: Superuser user object.
    :return: 204 response.
    """
    genre = await crud.genre.get(_id=genre_id)

    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    await crud.genre.remove(_id=genre_id)

    return Response(status_code=204)
