from datetime import datetime
from pydantic import ConfigDict

from src.entities import SerializerModel
from src.utils.enums import TransactionTypeEnum


class CategorySerializer(SerializerModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int | None
    name: str
    type: TransactionTypeEnum
    created_at: datetime
