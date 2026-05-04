from datetime import date

from src.entities.transaction.model import Transaction
from src.entities.transaction.repository import TransactionRepository
from src.utils.enums import TransactionTypeEnum
from src.routes.dashboard.requests import DashboardSummaryRequest


class DashboardService:
    """Service for dashboard operations."""

    async def get_summary(
        self,
        transaction_repository: TransactionRepository,
        user_id: int,
        month: int | None = None,
        year: int | None = None,
    ) -> dict:
        """
        Get dashboard summary for a given month and year.

        Returns:
            - total_income: Sum of all income transactions
            - total_expenses: Sum of all expense transactions
            - balance: income - expenses
            - recent_movements: List of recent movements for that month
        """
        # Get date range
        from_date, to_date = DashboardSummaryRequest.get_date_range(
            month, year)

        # Get all transactions for the month
        transactions = await transaction_repository.get_all_for_user(
            user_id,
            from_date=from_date,
            to_date=to_date,
        )

        # Calculate totals
        total_income = sum(
            t.amount for t in transactions
            if t.type == TransactionTypeEnum.INCOME
        )
        total_expenses = sum(
            t.amount for t in transactions
            if t.type == TransactionTypeEnum.EXPENSE
        )
        balance = total_income - total_expenses

        # Get recent movements (sorted by date descending, latest first)
        recent_movements = sorted(
            transactions,
            key=lambda t: t.date,
            reverse=True
        )

        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "balance": balance,
            "recent_movements": recent_movements,
        }
