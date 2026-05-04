from datetime import date as dateType
from pydantic import Field
from src.entities import SerializerModel
from src.utils.enums import DebtTypeEnum, DebtStatusEnum


class DebtCreate(SerializerModel):
    type: DebtTypeEnum
    person_name: str = Field(min_length=1, max_length=100)
    amount: float = Field(gt=0)
    date: dateType
    status: DebtStatusEnum
    note: str | None = Field(None, max_length=500)


class DebtUpdate(SerializerModel):
    type: DebtTypeEnum | None = None
    person_name: str | None = Field(None, min_length=1, max_length=100)
    amount: float | None = Field(None, gt=0)
    date: dateType | None = None
    status: DebtStatusEnum | None = None
    note: str | None = Field(None, max_length=500)
    transaction_id: int | None = None
