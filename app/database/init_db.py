import asyncio

from app.database.connection import engine, Base
from app.models.books_model import Book

# async function to create the tables in the database
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Tables created successfully.")
    print("Tables:", list(Base.metadata.tables.keys()))


async def main():
    try:
        await create_tables()
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())
