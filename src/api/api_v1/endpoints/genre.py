from typing import List
from fastapi import APIRouter, HTTPException, Response

from src import crud
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


@router.post("/", responses={409: {"description": "Genre already exists"}})
async def create_genre(genre: GenreCreate) -> GenreRead:
    """
    Create new genre.

    :param genre: Genre object.
    :return: Created genre object.
    """
    genre = await crud.genre.create(obj_in=genre)
    return genre


@router.put(
    "/{genre_id}",
    responses={
        404: {"description": "Genre not found"},
        409: {"description": "Genre already exists"},
    }
)
async def update_genre(genre_id: int, genre_new: GenreUpdate) -> GenreRead:
    """
    Update genre by id.

    :param genre_id: Genre id.
    :param genre_new: New genre object.
    :return: Updated genre object.
    """
    genre = await crud.genre.get(_id=genre_id)

    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    genre = await crud.genre.update(obj_current=genre, obj_new=genre_new)
    return genre


@router.delete("/{genre_id}", responses={404: {"description": "Genre not found"}})
async def delete_genre(genre_id: int) -> Response:
    """
    Delete genre by id.

    :param genre_id: Genre id.
    :return: 204 response.
    """
    genre = await crud.genre.get(_id=genre_id)

    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    await crud.genre.remove(_id=genre_id)

    return Response(status_code=204)
