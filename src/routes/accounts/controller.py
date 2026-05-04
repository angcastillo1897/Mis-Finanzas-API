from src.dependencies.async_db import AsyncSessionDepends
from src.dependencies.auth import CurrentUserDepends
from src.entities.account.repository import AccountRepository
from src.entities.account.serializer import AccountSerializer
from src.entities.user.model import User
from src.routes.accounts.requests import CreateAccountRequest, UpdateAccountRequest
from src.routes.accounts.responses import AccountResponse, AccountListResponse
from src.routes.accounts.service import AccountService


class AccountController:
    def __init__(self) -> None:
        self.service = AccountService()

    async def get_all_accounts(
        self,
        user: CurrentUserDepends,
        async_session: AsyncSessionDepends,
    ) -> AccountListResponse:
        """Get all accounts for the current user."""
        accounts = await self.service.get_all_accounts(
            AccountRepository(async_session),
            user.id,
        )
        return AccountListResponse(
            data=[AccountSerializer.model_validate(
                account) for account in accounts]
        )

    async def create_account(
        self,
        payload: CreateAccountRequest,
        user: CurrentUserDepends,
        async_session: AsyncSessionDepends,
    ) -> AccountResponse:
        """Create a new account for the current user."""
        account = await self.service.create_account(
            AccountRepository(async_session),
            user.id,
            payload,
        )
        return AccountResponse(
            data=AccountSerializer.model_validate(account)
        )

    async def update_account(
        self,
        account_id: int,
        payload: UpdateAccountRequest,
        user: CurrentUserDepends,
        async_session: AsyncSessionDepends,
    ) -> AccountResponse:
        """Update an existing account."""
        account = await self.service.update_account(
            AccountRepository(async_session),
            account_id,
            user.id,
            payload,
        )
        return AccountResponse(
            data=AccountSerializer.model_validate(account)
        )

    async def delete_account(
        self,
        account_id: int,
        user: CurrentUserDepends,
        async_session: AsyncSessionDepends,
    ) -> dict:
        """Delete an account."""
        await self.service.delete_account(
            AccountRepository(async_session),
            account_id,
            user.id,
        )
        return {"message": "Cuenta eliminada exitosamente"}

    async def recalculate_account_balance(
        self,
        account_id: int,
        user: CurrentUserDepends,
        async_session: AsyncSessionDepends,
    ) -> AccountResponse:
        """Recalculate account balance from all transactions (for data integrity verification)."""
        account = await self.service.recalculate_account_balance(
            AccountRepository(async_session),
            account_id,
            user.id,
        )
        return AccountResponse(
            data=AccountSerializer.model_validate(account)
        )
