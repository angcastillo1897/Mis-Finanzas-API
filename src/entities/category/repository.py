from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.entities import RepositoryBase
from src.entities.category.model import Category
from src.utils.enums import TransactionTypeEnum


class CategoryRepository(RepositoryBase[Category]):
    def __init__(self, async_session: AsyncSession) -> None:
        self.async_session = async_session

    async def get_by_id(self, category_id: int) -> Category | None:
        result = await self.async_session.execute(
            select(Category).where(Category.id == category_id)
        )
        return result.scalar_one_or_none()

    async def get_all_for_user(
        self,
        user_id: int,
        category_type: TransactionTypeEnum | None = None,
    ) -> list[Category]:
        """Get global categories and user-specific categories, optionally filtered by type."""
        query = select(Category).where(
            # Global categories (user_id IS NULL) OR user's own categories
            (Category.user_id.is_(None)) | (Category.user_id == user_id)
        )

        # Filter by type if provided
        if category_type:
            query = query.where(Category.type == category_type)

        result = await self.async_session.execute(query)
        return list(result.scalars().all())

    async def get_by_user_id(
        self,
        user_id: int,
        category_type: TransactionTypeEnum | None = None,
    ) -> list[Category]:
        """Get only user-specific categories, optionally filtered by type."""
        query = select(Category).where(Category.user_id == user_id)

        if category_type:
            query = query.where(Category.type == category_type)

        result = await self.async_session.execute(query)
        return list(result.scalars().all())

    async def create(self, category: Category) -> Category:
        self.async_session.add(category)
        await self.async_session.flush()
        return category

    async def update(self, category: Category) -> Category:
        await self.async_session.merge(category)
        await self.async_session.flush()
        return category

    async def delete(self, category: Category) -> None:
        await self.async_session.delete(category)
        await self.async_session.flush()
