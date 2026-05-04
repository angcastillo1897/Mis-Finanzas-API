from src.entities.transaction.serializer import TransactionSerializer
from src.entities import SerializerModel


class MovementResponse(SerializerModel):
    data: TransactionSerializer


class MovementListResponse(SerializerModel):
    data: list[TransactionSerializer]
