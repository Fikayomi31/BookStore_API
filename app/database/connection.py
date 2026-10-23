from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, create_async_engine

DATABASE_URL = "sqlite+aiosqlite:///./test.db"


engine =  create_async_engine(
    DATABASE_URL,
    echo=True,
)

Base = declarative_base()

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)



async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
        