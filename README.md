# BookStore API

A RESTful API for managing a collection of books, built with **FastAPI**, **Pydantic**, and **asynchronous SQLAlchemy**. The project demonstrates backend development fundamentals, including CRUD operations, request validation, database integration, search, sorting, and structured HTTP error handling.

## Features

- **Book management:** Create, retrieve, update, and delete books.
- **Data validation:** Validate titles, authors, descriptions, prices, publication years, and genres with Pydantic.
- **Genre validation:** Use a predefined set of book genres through a Python enum.
- **Search:** Filter books by title and author.
- **Sorting:** Sort books by title, author, price, or publication year in ascending or descending order.
- **Duplicate detection:** Prevent duplicate books with matching titles and authors through API-level checks.
- **Error handling:** Return appropriate HTTP status codes for missing books, duplicate submissions, invalid input, and database failures.
- **Asynchronous database operations:** Use SQLAlchemy's asynchronous API with SQLite.
- **Interactive API documentation:** Explore and test endpoints using Swagger UI.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| FastAPI | API framework |
| Pydantic | Request validation and response serialization |
| SQLAlchemy | ORM and database access |
| SQLite | Database storage |
| aiosqlite | Asynchronous SQLite driver |
| Uvicorn | ASGI development server |
| HTTPX | HTTP requests in API tests |

## Project Structure

```text
BookStore_API/
├── app/
│   ├── database/
│   │   ├── connection.py
│   │   └── init_db.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── books_model.py
│   │   └── genres.py
│   ├── routers/
│   │   └── books.py
│   └── schemas/
│       └── book_schema.py
├── tests/
│   └── test_books.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

*The `tests/` folder is used for automated tests. Add it if it has not yet been created. Your exact structure may differ slightly depending on the files in your project.*

## Getting Started

### 1. Prerequisites

Install the following:

- Python 3.12 or a compatible supported version
- Git (optional, for version control)
- Visual Studio Code or another code editor

### 2. Clone the Repository

If the project is hosted on GitHub:

```bash
git clone <your-repository-url>
cd BookStore_API
```

Alternatively, open your existing local project directory.

### 3. Create a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt instead:

```cmd
venv\Scripts\activate.bat
```

### 4. Install Dependencies

If `requirements.txt` already exists:

```powershell
python -m pip install -r requirements.txt
```

Otherwise, install the main dependencies:

```powershell
python -m pip install fastapi "uvicorn[standard]" sqlalchemy aiosqlite pydantic
```

Save your installed dependencies when ready:

```powershell
python -m pip freeze > requirements.txt
```

### 5. Initialize the Database

If your project uses `app/database/init_db.py` to create tables, run:

```powershell
python -m app.database.init_db
```

Run this command from the project root, and only if the initializer supports module execution as shown.

The database connection should use an asynchronous SQLite URL similar to:

```python
DATABASE_URL = "sqlite+aiosqlite:///./bookstore.db"
```

The actual database location depends on your configured URL and the working directory. Keep your database file out of version control.

### 6. Start the Development Server

From the project root, run:

```powershell
uvicorn main:app --reload
```

The API should be available at:

- API base URL: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

The book endpoints use the `/api/books` prefix.

| Method | Endpoint | Description | Expected success |
|---|---|---|---|
| GET | `/` | Welcome message | 200 OK |
| GET | `/health` | Health check | 200 OK |
| POST | `/api/books` | Create a book | 201 Created |
| GET | `/api/books` | List and search books | 200 OK |
| GET | `/api/books/{book_id}` | Retrieve one book | 200 OK |
| PUT | `/api/books/{book_id}` | Replace a book's editable fields | 200 OK |
| DELETE | `/api/books/{book_id}` | Delete a book | 204 No Content |

### Create a Book

**Request**

`POST /api/books`

```json
{
  "title": "Clean Code",
  "author": "Robert C. Martin",
  "description": "A guide to writing maintainable software.",
  "genre": "Technology",
  "price": 12000,
  "published_year": 2008
}
```

A successful response contains the created book and its database-generated ID.

```json
{
  "id": 1,
  "title": "Clean Code",
  "author": "Robert C. Martin",
  "description": "A guide to writing maintainable software.",
  "genre": "Technology",
  "price": 12000,
  "published_year": 2008
}
```

The ID shown is illustrative; the actual value depends on your database.

### Retrieve All Books

**Request**

`GET /api/books`

Returns the collection of books as a JSON array.

### Search by Title or Author

Search for books with a title containing a keyword:

```http
GET /api/books?title=clean
```

Search by author:

```http
GET /api/books?author=martin
```

Combine both filters:

```http
GET /api/books?title=clean&author=martin
```

Searches use case-insensitive partial matching, subject to the database's behavior.

### Sort Books

Sort by title in ascending order:

```http
GET /api/books?sort_by=title&order=asc
```

Sort by price from highest to lowest:

```http
GET /api/books?sort_by=price&order=desc
```

Supported `sort_by` values:

- `title`
- `author`
- `price`
- `published_year`

Supported `order` values:

- `asc`
- `desc`

### Retrieve One Book

```http
GET /api/books/1
```

Replace `1` with the desired book ID.

### Update a Book

```http
PUT /api/books/1
```

Send the complete set of required fields in the request body. This endpoint uses full-update semantics; it is not a partial-update endpoint.

### Delete a Book

```http
DELETE /api/books/1
```

A successful deletion returns `204 No Content`, with no response body.

## Data Validation

Pydantic schemas validate incoming data before the endpoint performs database writes.

| Field | Validation |
|---|---|
| `title` | Required; 1–200 characters; whitespace-only values rejected |
| `author` | Required; 1–100 characters; whitespace-only values rejected |
| `description` | Optional; maximum 500 characters |
| `genre` | Must match a defined `BookGenre` enum value |
| `price` | Must be greater than zero and finite |
| `published_year` | Optional; between 1 and 2100 under the current schema |

Invalid request data normally returns `422 Unprocessable Entity`.

## Error Handling

The API uses standard HTTP status codes to communicate outcomes.

| Status | Meaning |
|---|---|
| `200 OK` | Request succeeded |
| `201 Created` | A book was created |
| `204 No Content` | A book was deleted successfully |
| `404 Not Found` | The requested book ID does not exist |
| `409 Conflict` | A duplicate title-author combination was detected |
| `422 Unprocessable Entity` | Request data failed validation |
| `500 Internal Server Error` | An unexpected database operation failure occurred |

Database write operations should roll back failed transactions before returning an error. Error responses should not expose internal stack traces or database details.

Duplicate detection currently occurs at the API level. For stronger protection against simultaneous requests, a database-level uniqueness strategy should also be considered.

## Database Design

The `Book` SQLAlchemy model represents the `books` table. Its fields include:

- `id` — primary key
- `title` — book title
- `author` — author's name
- `description` — optional description
- `published_year` — optional publication year
- `genre` — predefined genre
- `price` — book price

The application uses SQLAlchemy's asynchronous sessions to perform database operations.

### Database Initialization

The project uses a lightweight initializer to create tables. SQLAlchemy's `create_all()` can create missing tables, but it does not automatically migrate an existing table when the model changes. For this learning project, schema changes may need to be handled manually.


## Running the Application

A typical development workflow is:

1. Activate the virtual environment.
2. Install dependencies.
3. Initialize the database when necessary.
4. Start Uvicorn.
5. Explore endpoints in Swagger UI.


## Learning Objectives

This project provides practical experience with:

- Building REST APIs using FastAPI
- Designing request and response schemas with Pydantic
- Using asynchronous SQLAlchemy sessions
- Modeling relational data
- Implementing CRUD operations
- Filtering and sorting API results
- Handling validation errors and HTTP exceptions

## Author

Fikayo Ogundijo

Backend development project built as part of a Python + FastAPI Backend Development Internship
by Datheon