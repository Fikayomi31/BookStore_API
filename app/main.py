from fastapi import FastAPI

from app.routers.books import router as books_router


app = FastAPI(
    title="BookStore REST API",
    description="A simple REST API for managing a bookstore",
    version="1.0.0"
)

@app.get("/")
async def home():
    return {
        "message": "Welcome to the BookStore REST API!"
    }


app.include_router(books_router)