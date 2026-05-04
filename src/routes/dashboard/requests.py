from typing import Optional
from pydantic import BaseModel, Field
from datetime import date, timedelta
import calendar


class DashboardSummaryRequest(BaseModel):
    """Request model for dashboard summary query parameters."""
    month: Optional[int] = Field(
        None,
        ge=1,
        le=12,
        description="Month (1-12). If not provided, uses current month"
    )
    year: Optional[int] = Field(
        None,
        ge=2000,
        description="Year. If not provided, uses current year"
    )

    @staticmethod
    def get_date_range(month: int | None, year: int | None) -> tuple[date, date]:
        """Get start and end date for the given month and year."""
        today = date.today()

        # Use current month/year if not provided
        if month is None:
            month = today.month
        if year is None:
            year = today.year

        # First day of the month
        from_date = date(year, month, 1)

        # Last day of the month
        _, last_day = calendar.monthrange(year, month)
        to_date = date(year, month, last_day)

        return from_date, to_date
