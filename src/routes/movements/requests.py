from src.entities.transaction.schemas import TransactionCreate, TransactionUpdate


class CreateMovementRequest(TransactionCreate):
    pass


class UpdateMovementRequest(TransactionUpdate):
    pass
