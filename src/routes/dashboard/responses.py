from src.entities.transaction.serializer import TransactionSerializer
from src.entities import SerializerModel


class DashboardSummarySerializer(SerializerModel):
    """Serializer for dashboard summary data."""
    total_income: float
    total_expenses: float
    balance: float
    recent_movements: list[TransactionSerializer]


class DashboardSummaryResponse(SerializerModel):
    """Response model for dashboard summary."""
    data: DashboardSummarySerializer
