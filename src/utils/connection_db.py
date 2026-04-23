from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy_utils import create_database, database_exists  # type: ignore

from src.settings import setting

uri: URL = URL.create(
    "postgresql+asyncpg",
    username=setting.BD_USERNAME,
    password=setting.BD_PASSWORD,
    host=setting.BD_HOST,
    port=int(setting.BD_PORT),
    database=setting.BD_NAME,
)
async_engine: AsyncEngine = create_async_engine(uri, pool_pre_ping=True)
Async_session_local: async_sessionmaker[AsyncSession] = async_sessionmaker(
    autoflush=False, bind=async_engine, expire_on_commit=False, class_=AsyncSession
)


class Model(AsyncAttrs, DeclarativeBase):
    ...


def create_database_if_not_exist():
    if not database_exists(uri):
        create_database(uri)
