from typing import List
from fastapi import APIRouter, HTTPException, Response, Depends

from src import crud
from src.models import User
from src.api.deps import current_active_superuser
from src.schemas.author import AuthorRead, AuthorCreate, AuthorUpdate


router = APIRouter()


@router.get("/")
async def get_authors() -> List[AuthorRead]:
    """
    Get all authors.

    :return: List of genre author objects.
    """
    authors = await crud.author.get_multi()
    return authors


@router.get(
    "/{author_id}",
    responses={
        404: {"description": "Author not found"},
        409: {"description": "Author already exists"},
    }
)
async def get_author_by_id(author_id: int) -> AuthorRead:
    """
    Get author by id.

    :param author_id: Author id.
    :return: Author object.
    """
    author = await crud.author.get(_id=author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return author


@router.post("/", responses={409: {"description": "Author already exists"}}, status_code=201)
async def create_author(
    author_new: AuthorCreate,
    user: User = Depends(current_active_superuser)
) -> AuthorRead:
    """
    Create new author.

    Required role:
    - Superuser

    :param author_new: Author object.
    :param user: Superuser user object.
    :return: Created author object.
    """
    author = await crud.author.create(obj_in=author_new)
    return author


@router.put(
    "/{author_id}",
    responses={
        404: {"description": "Author not found"},
        409: {"description": "Author already exists"},
    }
)
async def update_author(
    author_id: int,
    author_new: AuthorUpdate,
    user: User = Depends(current_active_superuser)
) -> AuthorRead:
    """
    Update author by id.

    Required role:
    - Superuser

    :param author_id: Author id.
    :param author_new: New author object.
    :param user: Superuser user object.
    :return: Updated author object.
    """
    author = await crud.author.get(_id=author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    author = await crud.author.update(obj_current=author, obj_new=author_new)
    return author


@router.delete("/{author_id}", responses={404: {"description": "Author not found"}})
async def delete_author(
    author_id: int,
    user: User = Depends(current_active_superuser)
) -> Response:
    """
    Delete author by id.

    Required role:
    - Superuser

    :param author_id: Author id.
    :param user: Superuser user object.
    :return: 204 response.
    """
    author = await crud.author.get(_id=author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    await crud.author.remove(_id=author_id)

    return Response(status_code=204)
