from fastapi import Query

from src.dependencies.async_db import AsyncSessionDepends
from src.dependencies.auth import CurrentUserDepends
from src.entities.debt.repository import DebtRepository
from src.entities.debt.serializer import DebtSerializer
from src.entities.transaction.repository import TransactionRepository
from src.routes.debts.requests import CreateDebtRequest, UpdateDebtRequest
from src.routes.debts.responses import DebtResponse, DebtListResponse
from src.routes.debts.service import DebtService


class DebtController:
    def __init__(self) -> None:
        self.service = DebtService()

    async def get_all_debts(
        self,
        user: CurrentUserDepends,
        async_session: AsyncSessionDepends,
        type: str | None = Query(
            None, description="Filter by debt type: I_OWE or THEY_OWE_ME"),
        status: str | None = Query(
            None, description="Filter by debt status: PENDING or PAID"),
    ) -> DebtListResponse:
        """Get all debts for the current user with optional filters."""
        debts = await self.service.get_all_debts(
            DebtRepository(async_session),
            user.id,
            type,
            status,
        )
        return DebtListResponse(
            data=[DebtSerializer.model_validate(debt) for debt in debts]
        )

    async def get_debt_by_id(
        self,
        debt_id: int,
        user: CurrentUserDepends,
        async_session: AsyncSessionDepends,
    ) -> DebtResponse:
        """Get a specific debt."""
        debt = await self.service.get_debt_by_id(
            DebtRepository(async_session),
            debt_id,
            user.id,
        )
        return DebtResponse(
            data=DebtSerializer.model_validate(debt)
        )

    async def create_debt(
        self,
        payload: CreateDebtRequest,
        user: CurrentUserDepends,
        async_session: AsyncSessionDepends,
    ) -> DebtResponse:
        """Create a new debt (independent of transactions)."""
        debt = await self.service.create_debt(
            DebtRepository(async_session),
            user.id,
            payload,
        )
        return DebtResponse(
            data=DebtSerializer.model_validate(debt)
        )

    async def update_debt(
        self,
        debt_id: int,
        payload: UpdateDebtRequest,
        user: CurrentUserDepends,
        async_session: AsyncSessionDepends,
    ) -> DebtResponse:
        """Update a debt and optionally link it to a transaction when paid."""
        debt = await self.service.update_debt(
            DebtRepository(async_session),
            TransactionRepository(async_session),
            debt_id,
            user.id,
            payload,
        )
        return DebtResponse(
            data=DebtSerializer.model_validate(debt)
        )

    async def delete_debt(
        self,
        debt_id: int,
        user: CurrentUserDepends,
        async_session: AsyncSessionDepends,
    ) -> dict:
        """Delete a debt."""
        await self.service.delete_debt(
            DebtRepository(async_session),
            debt_id,
            user.id,
        )
        return {"message": "Deuda eliminada exitosamente"}
