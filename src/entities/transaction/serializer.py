from datetime import date, datetime
from pydantic import ConfigDict

from src.entities import SerializerModel
from src.utils.enums import TransactionTypeEnum


class TransactionSerializer(SerializerModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    account_id: int
    category_id: int
    type: TransactionTypeEnum
    amount: float
    date: date
    note: str | None
    created_at: datetime
