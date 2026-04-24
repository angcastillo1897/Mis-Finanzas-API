from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.connection_db import Model
from src.utils.helpers import to_camel_case

T = TypeVar("T", bound="Model")


class RepositoryBase(Generic[T]):
    """RepositoryBase.
    Use this class when you create a new Repository class to manage transactions"""

    def __init__(self, async_session: AsyncSession):
        self.async_session: AsyncSession = async_session

    async def commit(self):
        await self.async_session.commit()

    async def flush(self):
        await self.async_session.flush()

    async def rollback(self):
        await self.async_session.rollback()


class SerializerModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel_case,
        populate_by_name=True,
    )
