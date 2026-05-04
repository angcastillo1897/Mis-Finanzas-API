from src.entities.account.model import Account
from src.entities.account.repository import AccountRepository
from src.entities.account.schemas import AccountCreate, AccountUpdate
from src.exceptions.not_found import NotFoundException
from src.exceptions.forbidden_exception import ForbiddenException


class AccountService:
    async def get_all_accounts(
        self,
        account_repository: AccountRepository,
        user_id: int,
    ) -> list[Account]:
        """Get all accounts for a specific user."""
        accounts = await account_repository.get_by_user_id(user_id)
        return accounts

    async def get_account_by_id(
        self,
        account_repository: AccountRepository,
        account_id: int,
        user_id: int,
    ) -> Account:
        """Get a specific account, validating ownership."""
        account = await account_repository.get_by_id(account_id)

        if not account:
            raise NotFoundException(
                f"Cuenta con ID {account_id} no encontrada")

        if account.user_id != user_id:
            raise ForbiddenException(
                "No tienes permiso para acceder esta cuenta")

        return account

    async def create_account(
        self,
        account_repository: AccountRepository,
        user_id: int,
        payload: AccountCreate,
    ) -> Account:
        """Create a new account for the user."""
        new_account = Account(
            user_id=user_id,
            name=payload.name,
            type=payload.type,
            balance=payload.balance,
        )

        await account_repository.create(new_account)
        await account_repository.commit()

        return new_account

    async def update_account(
        self,
        account_repository: AccountRepository,
        account_id: int,
        user_id: int,
        payload: AccountUpdate,
    ) -> Account:
        """Update an existing account."""
        account = await self.get_account_by_id(
            account_repository, account_id, user_id
        )

        # Update only provided fields
        if payload.name is not None:
            account.name = payload.name
        if payload.type is not None:
            account.type = payload.type
        if payload.balance is not None:
            account.balance = payload.balance

        await account_repository.update(account)
        await account_repository.commit()

        return account

    async def delete_account(
        self,
        account_repository: AccountRepository,
        account_id: int,
        user_id: int,
    ) -> None:
        """Delete an account."""
        account = await self.get_account_by_id(
            account_repository, account_id, user_id
        )

        await account_repository.delete(account)
        await account_repository.commit()

    async def recalculate_account_balance(
        self,
        account_repository: AccountRepository,
        account_id: int,
        user_id: int,
    ) -> Account:
        """Recalculate account balance from all transactions for data integrity verification."""
        account = await self.get_account_by_id(
            account_repository, account_id, user_id
        )

        # Recalculate balance from transactions
        calculated_balance = await account_repository.recalculate_balance(account_id)

        # Update account with recalculated balance
        account.balance = calculated_balance
        await account_repository.update(account)
        await account_repository.commit()

        return account
