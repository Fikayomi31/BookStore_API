from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.models.books_model import Book
from app.schemas.book_schema import BookCreate, BookUpdate, BookResponse

router = APIRouter(
    prefix="/api/books",
    tags=["books"]
)

@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)

async def create_book(
    book_data: BookCreate, 
    db: AsyncSession = Depends(get_db)
):

    try:
        # Check whether the same book already exists
        statement = select(Book).where(
                Book.title.ilike(book_data.title.strip()),
                Book.author.ilike(book_data.author.strip())
            )
        result = await db.execute(statement)

        existing_book = result.scalars().first()
        if existing_book:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Book with the same title and author already exists"
            )
        
        # Create  a new book 
        new_book = Book(**book_data.model_dump())


        db.add(new_book)
        await db.commit()
        await db.refresh(new_book)

        return new_book

    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create book"
        )



@router.get("", response_model=list[BookResponse])
async def get_book(
    title: str | None = Query(default=None, max_length=200),
    author: str | None = Query(default=None, max_length=200),
    sort_by: Literal["title", "author", "price", "published_year"] = "title",
    order: Literal["asc", "desc"] = "asc",
    db: AsyncSession = Depends(get_db)
):
    statement = select(Book)

    if title and title.strip():
        statement = statement.where(
            Book.title.ilike(f"%{title.strip()}%")
        )

    if author and author.strip():
        statement = statement.where(
            Book.author.ilike(f"%{author.strip()}%")
        )

    sort_column = getattr(Book, sort_by)

    if order == "asc":
        statement = statement.order_by(sort_column.asc())
    else:
        statement = statement.order_by(sort_column.desc())

    try:
        result = await db.execute(statement)
        books = result.scalars().all()

        return list(books)

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve books"
        )

    
# Get book by ID
@router.get("/{book_id}", response_model=BookResponse)
async def get_book_id(book_id: int, db: AsyncSession = Depends(get_db)):

    try:
        book = await db.get(Book, book_id)

        if book is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        
        return book
    except HTTPException:
        raise

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve book"
        )

# Update book by ID
@router.put("/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: int, 
    book_data: BookCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        book = await db.get(Book, book_id)

        if book is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )

        # prevent updating to a title and author that already exists in another book
        statement = select(Book).where(
            Book.title.ilike(book_data.title),
            Book.author.ilike(book_data.author),
            Book.id != book_id
        )

        result = await db.execute(statement)
        existing_book = result.scalars().first()

        if existing_book:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Another book with the same title and author already exists"
            )
        
        update_data = book_data.model_dump()
        for key, value in update_data.items():
            setattr(book, key, value)
        await db.commit()
        await db.refresh(book)

        return book
    except HTTPException:
        raise

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to update book"
        )


# Delete a book
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):

    try:
        book = await db.get(Book, book_id)

        if book is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        
        await db.delete(book)
        await db.commit()

    except HTTPException:
        raise

    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to delete book"
        )

    return None