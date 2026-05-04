from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.entities import RepositoryBase
from src.entities.debt.model import Debt
from src.utils.enums import DebtTypeEnum, DebtStatusEnum


class DebtRepository(RepositoryBase[Debt]):
    def __init__(self, async_session: AsyncSession) -> None:
        self.async_session = async_session

    async def get_by_id(self, debt_id: int) -> Debt | None:
        result = await self.async_session.execute(
            select(Debt).where(Debt.id == debt_id)
        )
        return result.scalar_one_or_none()

    async def get_all_for_user(
        self,
        user_id: int,
        debt_type: DebtTypeEnum | None = None,
        status: DebtStatusEnum | None = None,
    ) -> list[Debt]:
        """Get all debts for a user, optionally filtered by type and status."""
        conditions = [Debt.user_id == user_id]

        if debt_type:
            conditions.append(Debt.type == debt_type)
        if status:
            conditions.append(Debt.status == status)

        from sqlalchemy import and_
        query = select(Debt).where(and_(*conditions))
        result = await self.async_session.execute(query)
        return list(result.scalars().all())

    async def create(self, debt: Debt) -> Debt:
        self.async_session.add(debt)
        await self.async_session.flush()
        return debt

    async def update(self, debt: Debt) -> Debt:
        await self.async_session.merge(debt)
        await self.async_session.flush()
        return debt

    async def delete(self, debt: Debt) -> None:
        await self.async_session.delete(debt)
        await self.async_session.flush()
