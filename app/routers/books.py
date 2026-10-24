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