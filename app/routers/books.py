from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.models.books_model import Book
from app.schemas.book_schema import BookCreate, BookUpdate, BookResponse

router = APIRouter(
    prefix="/api/books",
    tags=["books"]
)

@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)

async def create_book(book_data: BookCreate, db: AsyncSession = Depends(get_db)):

    # Validated pylandic model data is converted to a SQLAlchemy model instance
    new_book = Book(**book_data.model_dump())

    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)

    return new_book

@router.get("", response_model=list[BookResponse])
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Book))
    books = result.scalars().all()

    return books

@router.get("/{book_id}", response_model=BookResponse)
async def get_book_id(book_id: int, db: AsyncSession = Depends(get_db)):

    book = await db.get(Book, book_id)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    return book

@router.put("/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: int, 
    book_data: BookCreate,
    db: AsyncSession = Depends(get_db)
):
    book = await db.get(Book, book_id)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    update_data = book_data.model_dump()
    for key, value in update_data.items():
        setattr(book, key, value)

    await db.commit()
    await db.refresh(book)

    return book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):

    book = await db.get(Book, book_id)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    await db.delete(book)
    await db.commit()

    return None