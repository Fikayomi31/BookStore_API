from pydantic import BaseModel, Field, ConfigDict, field_validator

from app.models.genres import BookGenre

"""
A Pydantic model for book creation, update, and response.
"""

class BookCreate(BaseModel):

    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=500)
    genre: BookGenre
    price : float = Field(gt=0)
    published_year: int | None = Field(default=None, ge=1, le=2100)

    @field_validator("title", "author")
    @classmethod
    def clean_required_text(cls, value: str) -> str:
        value = value.strip()
        
        if not value:
            raise ValueError("Field cannot be empty or whitespace")
        
        return value

class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    author: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    genre: BookGenre | None = Field(default="Fiction")
    price : float | None = Field(default=None, gt=0, allow_inf_nan=False)
    published_year: int | None = Field(default=None, ge=1, le=2100)

    @field_validator("title", "author")
    @classmethod
    def clean_optional_text(cls, value: str | None) -> str | None:
        
        if value is not None:
            value = value.strip()
            if not value:
                raise ValueError("Field cannot be empty or whitespace")
        return value
    

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    description: str | None
    genre: BookGenre
    price : float
    published_year: int 

    model_config = ConfigDict(from_attributes=True)