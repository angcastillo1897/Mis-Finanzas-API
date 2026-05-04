from datetime import date, datetime
from pydantic import ConfigDict

from src.entities import SerializerModel
from src.utils.enums import DebtTypeEnum, DebtStatusEnum


class DebtSerializer(SerializerModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    type: DebtTypeEnum
    person_name: str
    amount: float
    date: date
    status: DebtStatusEnum
    note: str | None
    transaction_id: int | None
    created_at: datetime
    updated_at: datetime
