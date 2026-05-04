from datetime import date

from fastapi import Query

from src.dependencies.async_db import AsyncSessionDepends
from src.dependencies.auth import CurrentUserDepends
from src.entities.transaction.repository import TransactionRepository
from src.entities.transaction.serializer import TransactionSerializer
from src.entities.account.repository import AccountRepository
from src.entities.category.repository import CategoryRepository
from src.routes.movements.requests import CreateMovementRequest, UpdateMovementRequest
from src.routes.movements.responses import MovementResponse, MovementListResponse
from src.routes.movements.service import MovementService


class MovementController:
    def __init__(self) -> None:
        self.service = MovementService()

    async def get_all_movements(
        self,
        user: CurrentUserDepends,
        async_session: AsyncSessionDepends,
        type: str | None = Query(
            None, description="Filter by movement type: ingreso or gasto"),
        category_id: int | None = Query(
            None, description="Filter by category ID"),
        account_id: int | None = Query(
            None, description="Filter by account ID"),
        from_date: date | None = Query(
            None, description="Filter from date (YYYY-MM-DD)"),
        to_date: date | None = Query(
            None, description="Filter to date (YYYY-MM-DD)"),
    ) -> MovementListResponse:
        """Get all movements for the current user with optional filters."""
        movements = await self.service.get_all_movements(
            TransactionRepository(async_session),
            user.id,
            type,
            category_id,
            account_id,
            from_date,
            to_date,
        )
        return MovementListResponse(
            data=[TransactionSerializer.model_validate(
                movement) for movement in movements]
        )

    async def get_movement_by_id(
        self,
        movement_id: int,
        user: CurrentUserDepends,
        async_session: AsyncSessionDepends,
    ) -> MovementResponse:
        """Get a specific movement."""
        movement = await self.service.get_movement_by_id(
            TransactionRepository(async_session),
            movement_id,
            user.id,
        )
        return MovementResponse(
            data=TransactionSerializer.model_validate(movement)
        )

    async def create_movement(
        self,
        payload: CreateMovementRequest,
        user: CurrentUserDepends,
        async_session: AsyncSessionDepends,
    ) -> MovementResponse:
        """Create a new movement for the current user."""
        movement = await self.service.create_movement(
            TransactionRepository(async_session),
            AccountRepository(async_session),
            CategoryRepository(async_session),
            user.id,
            payload,
        )
        return MovementResponse(
            data=TransactionSerializer.model_validate(movement)
        )

    async def update_movement(
        self,
        movement_id: int,
        payload: UpdateMovementRequest,
        user: CurrentUserDepends,
        async_session: AsyncSessionDepends,
    ) -> MovementResponse:
        """Update an existing movement."""
        movement = await self.service.update_movement(
            TransactionRepository(async_session),
            AccountRepository(async_session),
            CategoryRepository(async_session),
            movement_id,
            user.id,
            payload,
        )
        return MovementResponse(
            data=TransactionSerializer.model_validate(movement)
        )

    async def delete_movement(
        self,
        movement_id: int,
        user: CurrentUserDepends,
        async_session: AsyncSessionDepends,
    ) -> dict:
        """Delete a movement."""
        await self.service.delete_movement(
            TransactionRepository(async_session),
            AccountRepository(async_session),
            movement_id,
            user.id,
        )
        return {"message": "Movimiento eliminado exitosamente"}
