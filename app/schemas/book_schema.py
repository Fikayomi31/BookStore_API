from pydantic import BaseModel, Field, ConfigDict

from app.models.genres import BookGenre

"""
A Pydantic model for creating a new book.
"""

class BookCreate(BaseModel):

    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=500)
    genre: BookGenre
    price : float = Field(gt=0)
    published_year: int | None = Field(default=None, ge=0)

class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255, description="The title of the book")
    author: str | None = Field(default=None, min_length=1, max_length=255, description="The author of the book")
    description: str | None = Field(default=None, max_length=1000, description="A brief description of the book")
    genre: BookGenre | None = Field(default=None, description="The genre of the book")
    price : float | None = Field(default=None, gt=0, description="The price of the book")
    published_year: int | None = Field(default=None, ge=0, le=9999, description="The year the book was published")

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    description: str | None
    genre: BookGenre
    price : float
    published_year: int | None

    model_config = ConfigDict(from_attributes=True)