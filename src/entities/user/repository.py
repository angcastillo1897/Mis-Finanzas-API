from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.entities import RepositoryBase
from src.entities.user.model import User


class UserRepository(RepositoryBase[User]):
    def __init__(self, async_session: AsyncSession) -> None:
        self.async_session = async_session

    async def get_by_email(self, email: str) -> User | None:
        result = await self.async_session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.async_session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        self.async_session.add(user)
        await self.async_session.flush()
        return user

    # async def commit(self) -> None:
    #     await self.async_session.commit()

    # async def refresh(self, user: User) -> None:
    #     await self.async_session.refresh(user)
