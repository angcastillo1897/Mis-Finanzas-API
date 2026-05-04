from datetime import date as dateType
from pydantic import Field
from src.entities import SerializerModel
from src.utils.enums import TransactionTypeEnum


class TransactionCreate(SerializerModel):
    account_id: int = Field(gt=0)
    category_id: int = Field(gt=0)
    type: TransactionTypeEnum
    amount: float = Field(gt=0)
    date: dateType
    note: str | None = Field(None, max_length=500)


class TransactionUpdate(SerializerModel):
    account_id: int | None = Field(None, gt=0)
    category_id: int | None = Field(None, gt=0)
    type: TransactionTypeEnum | None = None
    amount: float | None = Field(None, gt=0)
    date: dateType | None = None
    note: str | None = Field(None, max_length=500)
