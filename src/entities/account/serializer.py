from datetime import datetime
from pydantic import ConfigDict

from src.entities import SerializerModel
from src.utils.enums import AccountTypeEnum


class AccountSerializer(SerializerModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    name: str
    type: AccountTypeEnum
    balance: float
    created_at: datetime
