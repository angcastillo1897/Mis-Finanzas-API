from pydantic import Field
from src.entities import SerializerModel
from src.utils.enums import TransactionTypeEnum


class CategoryCreate(SerializerModel):
    name: str = Field(min_length=1, max_length=100)
    type: TransactionTypeEnum


class CategoryUpdate(SerializerModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    type: TransactionTypeEnum | None = None
