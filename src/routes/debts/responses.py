from src.entities.debt.serializer import DebtSerializer
from src.entities import SerializerModel


class DebtResponse(SerializerModel):
    data: DebtSerializer


class DebtListResponse(SerializerModel):
    data: list[DebtSerializer]
