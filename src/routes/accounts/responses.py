from src.entities.account.serializer import AccountSerializer
from src.entities import SerializerModel


class AccountResponse(SerializerModel):
    data: AccountSerializer


class AccountListResponse(SerializerModel):
    data: list[AccountSerializer]
