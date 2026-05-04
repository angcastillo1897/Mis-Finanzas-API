from typing import Optional

from fastapi import Query

from src.dependencies.async_db import AsyncSessionDepends
from src.dependencies.auth import CurrentUserDepends
from src.entities.transaction.repository import TransactionRepository
from src.entities.transaction.serializer import TransactionSerializer
from src.routes.dashboard.responses import DashboardSummaryResponse, DashboardSummarySerializer
from src.routes.dashboard.service import DashboardService


class DashboardController:
    def __init__(self) -> None:
        self.service = DashboardService()

    async def get_summary(
        self,
        user: CurrentUserDepends,
        async_session: AsyncSessionDepends,
        month: Optional[int] = Query(
            None,
            ge=1,
            le=12,
            description="Month (1-12). If not provided, uses current month"
        ),
        year: Optional[int] = Query(
            None,
            ge=2000,
            description="Year. If not provided, uses current year"
        ),
    ) -> DashboardSummaryResponse:
        """Get dashboard summary for the current user."""
        summary = await self.service.get_summary(
            TransactionRepository(async_session),
            user.id,
            month,
            year,
        )

        return DashboardSummaryResponse(
            data=DashboardSummarySerializer(
                total_income=summary["total_income"],
                total_expenses=summary["total_expenses"],
                balance=summary["balance"],
                recent_movements=[
                    TransactionSerializer.model_validate(movement)
                    for movement in summary["recent_movements"]
                ],
            )
        )
