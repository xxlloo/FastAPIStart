from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from sqlmodel import SQLModel

from config.config import settings

async_engine = create_async_engine(settings.ASYNC_DATABASE_URI, echo=True, future=True)

Base = declarative_base()

session_local: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=async_engine, expire_on_commit=False, class_=AsyncSession
)


async def init_create_tables():
    async with async_engine.begin() as conn:
        try:
            await conn.run_sync(SQLModel.metadata.create_all)
            print("Tables created successfully!")
        except Exception as e:
            print(f"Error creating tables: {e}")
