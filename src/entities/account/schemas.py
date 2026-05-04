from pydantic import Field
from src.entities import SerializerModel
from src.utils.enums import AccountTypeEnum


class AccountCreate(SerializerModel):
    name: str = Field(min_length=1, max_length=100)
    type: AccountTypeEnum
    balance: float = Field(default=0.0, ge=0)


class AccountUpdate(SerializerModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    type: AccountTypeEnum | None = None
    balance: float | None = Field(None, ge=0)
