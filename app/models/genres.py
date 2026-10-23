from enum import Enum


class BookGenre(str, Enum):
    FICTION = "Fiction"
    NON_FICTION = "Non-Fiction"
    MYSTERY = "Mystery"
    FANTASY = "Fantasy"
    SCIENCE_FICTION = "Science Fiction"
    ROMANCE = "Romance"
    HORROR = "Horror"
    BIOGRAPHY = "Biography"
    HISTORY = "History"
    POETRY = "Poetry"
    BUSINESS = "Business"
    TECHNOLOGY = "Technology"
    FINANCE = "Finance"
    SELF_HELP = "Self-Help"