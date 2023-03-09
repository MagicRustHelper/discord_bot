from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core import app_config

engine = create_async_engine(app_config.SQLALCHEMY_DATABASE_URI)

SessinLocal = async_sessionmaker(
    autoflush=False,
    expire_on_commit=False,
    bind=engine,
)


@asynccontextmanager
async def get_session() -> AsyncSession:
    session = SessinLocal()
    try:
        yield session
    finally:
        await session.close()
