from typing import List, Annotated
from fastapi import APIRouter, HTTPException, Response, Query, Depends

from src import crud
from src.models import User
from src.api.deps import current_active_superuser
from src.models.book import BookCondition
from src.schemas.book import BookRead, BookCreate, BookUpdate


router = APIRouter()


@router.get("/")
async def get_books(
    genre: Annotated[str, Query(...)] = None,
    author: Annotated[str, Query(...)] = None,
    condition: Annotated[BookCondition, Query(...)] = None,
) -> List[BookRead]:
    """
    Get all books.

    :return: List of book objects.
    """
    books = await crud.book.filter_by_params(genre, author, condition)
    return books


@router.get(
    "/{book_id}",
    responses={
        404: {"description": "Book not found"},
        409: {"description": "Book already exists"},
    }
)
async def get_book_by_id(book_id: int) -> BookRead:
    """
    Get book by id.

    :param book_id: Book id.
    :return: Book object.
    """
    book = await crud.book.get(_id=book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@router.post("/", responses={409: {"description": "Book already exists"}})
async def create_book(
    book_new: BookCreate,
    user: User = Depends(current_active_superuser)
) -> BookRead:
    """
    Create new book.

    Required role:
    - Superuser

    :param book_new: Book object.
    :param user: Superuser user object.
    :return: Created book object.
    """
    # Check if genre exists
    genre = await crud.genre.get(_id=book_new.genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    # Check if author exists
    author = await crud.author.get(_id=book_new.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    book = await crud.book.create(obj_in=book_new)
    return book


@router.put(
    "/{author_id}",
    responses={
        404: {"description": "Book not found"},
        409: {"description": "Book already exists"},
    }
)
async def update_book(
    book_id: int,
    book_new: BookUpdate,
    user: User = Depends(current_active_superuser)
) -> BookRead:
    """
    Update book by id.

    Required role:
    - Superuser

    :param book_id: Book id.
    :param book_new: New book object.
    :param user: Superuser user object.
    :return: Updated book object.
    """
    # Check if book exists
    book = await crud.book.get(_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Check if genre exists
    genre = await crud.genre.get(_id=book_new.genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    # Check if author exists
    author = await crud.author.get(_id=book_new.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    book = await crud.book.update(obj_current=book, obj_new=book_new)
    return book


@router.delete("/{book_id}", responses={404: {"description": "Book not found"}})
async def delete_book(
    book_id: int,
    user: User = Depends(current_active_superuser)
) -> Response:
    """
    Delete book by id.

    Required role:
    - Superuser

    :param book_id: Book id.
    :param user: Superuser user object.
    :return: 204 response.
    """
    book = await crud.book.get(_id=book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    await crud.book.remove(_id=book_id)

    return Response(status_code=204)
