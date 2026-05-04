from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.entities import RepositoryBase
from src.entities.account.model import Account
from src.utils.enums import TransactionTypeEnum


class AccountRepository(RepositoryBase[Account]):
    def __init__(self, async_session: AsyncSession) -> None:
        self.async_session = async_session

    async def get_by_id(self, account_id: int) -> Account | None:
        result = await self.async_session.execute(
            select(Account).where(Account.id == account_id)
        )
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int) -> list[Account]:
        result = await self.async_session.execute(
            select(Account).where(Account.user_id == user_id)
        )
        return list(result.scalars().all())

    async def create(self, account: Account) -> Account:
        self.async_session.add(account)
        await self.async_session.flush()
        return account

    async def update(self, account: Account) -> Account:
        await self.async_session.merge(account)
        await self.async_session.flush()
        return account

    async def delete(self, account: Account) -> None:
        await self.async_session.delete(account)
        await self.async_session.flush()

    async def recalculate_balance(self, account_id: int) -> float:
        """Recalculate account balance from all transactions."""
        from src.entities.transaction.model import Transaction

        # Get all transactions for this account
        result = await self.async_session.execute(
            select(
                func.sum(
                    func.case(
                        (Transaction.type == TransactionTypeEnum.INCOME,
                         Transaction.amount),
                        else_=-Transaction.amount,
                    )
                )
            ).where(Transaction.account_id == account_id)
        )
        total_balance = result.scalar() or 0.0
        return float(total_balance)

    async def update_balance(self, account: Account, amount: float, is_income: bool) -> None:
        """Update account balance based on transaction type."""
        if is_income:
            account.balance += amount
        else:
            account.balance -= amount

        await self.update(account)
