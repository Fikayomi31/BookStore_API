from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy import Enum as EnumSQLAlchemy

from app.models.genres import BookGenre

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True, index=True)
    published_year = Column(Integer, nullable=True, index=True)
    genre = Column(EnumSQLAlchemy(BookGenre, name="book_genre"), nullable=False, index=True)

    def __repr__(self):
        return f"<Book(title='{self.title}', author='{self.author}', published_year={self.published_year})>"