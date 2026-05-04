from datetime import date
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.entities import RepositoryBase
from src.entities.transaction.model import Transaction
from src.utils.enums import TransactionTypeEnum


class TransactionRepository(RepositoryBase[Transaction]):
    def __init__(self, async_session: AsyncSession) -> None:
        self.async_session = async_session

    async def get_by_id(self, transaction_id: int) -> Transaction | None:
        result = await self.async_session.execute(
            select(Transaction).where(Transaction.id == transaction_id)
        )
        return result.scalar_one_or_none()

    async def get_all_for_user(
        self,
        user_id: int,
        transaction_type: TransactionTypeEnum | None = None,
        category_id: int | None = None,
        account_id: int | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[Transaction]:
        """Get all transactions for a user with optional filters."""
        conditions = [Transaction.user_id == user_id]

        if transaction_type:
            conditions.append(Transaction.type == transaction_type)
        if category_id:
            conditions.append(Transaction.category_id == category_id)
        if account_id:
            conditions.append(Transaction.account_id == account_id)
        if from_date:
            conditions.append(Transaction.date >= from_date)
        if to_date:
            conditions.append(Transaction.date <= to_date)

        query = select(Transaction).where(and_(*conditions))
        result = await self.async_session.execute(query)
        return list(result.scalars().all())

    async def create(self, transaction: Transaction) -> Transaction:
        self.async_session.add(transaction)
        await self.async_session.flush()
        return transaction

    async def update(self, transaction: Transaction) -> Transaction:
        await self.async_session.merge(transaction)
        await self.async_session.flush()
        return transaction

    async def delete(self, transaction: Transaction) -> None:
        await self.async_session.delete(transaction)
        await self.async_session.flush()
