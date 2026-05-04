from src.entities.debt.model import Debt
from src.entities.debt.repository import DebtRepository
from src.entities.debt.schemas import DebtCreate, DebtUpdate
from src.entities.transaction.repository import TransactionRepository
from src.exceptions.not_found import NotFoundException
from src.exceptions.forbidden_exception import ForbiddenException
from src.utils.enums import DebtTypeEnum, DebtStatusEnum


class DebtService:
    async def get_all_debts(
        self,
        debt_repository: DebtRepository,
        user_id: int,
        debt_type: str | None = None,
        status: str | None = None,
    ) -> list[Debt]:
        """Get all debts for a user, optionally filtered by type and status."""
        parsed_type = None
        parsed_status = None

        if debt_type:
            try:
                parsed_type = DebtTypeEnum(debt_type)
            except ValueError:
                raise ValueError(f"Tipo de deuda inválido: {debt_type}")

        if status:
            try:
                parsed_status = DebtStatusEnum(status)
            except ValueError:
                raise ValueError(f"Estado de deuda inválido: {status}")

        debts = await debt_repository.get_all_for_user(user_id, parsed_type, parsed_status)
        return debts

    async def get_debt_by_id(
        self,
        debt_repository: DebtRepository,
        debt_id: int,
        user_id: int,
    ) -> Debt:
        """Get a specific debt, validating ownership."""
        debt = await debt_repository.get_by_id(debt_id)

        if not debt:
            raise NotFoundException(f"Deuda con ID {debt_id} no encontrada")

        if debt.user_id != user_id:
            raise ForbiddenException(
                "No tienes permiso para acceder esta deuda")

        return debt

    async def create_debt(
        self,
        debt_repository: DebtRepository,
        user_id: int,
        payload: DebtCreate,
    ) -> Debt:
        """Create a new debt (independent, no transaction required)."""
        new_debt = Debt(
            user_id=user_id,
            type=payload.type,
            person_name=payload.person_name,
            amount=payload.amount,
            date=payload.date,
            status=payload.status,
            note=payload.note,
            transaction_id=None,
        )

        await debt_repository.create(new_debt)
        await debt_repository.commit()

        return new_debt

    async def update_debt(
        self,
        debt_repository: DebtRepository,
        transaction_repository: TransactionRepository,
        debt_id: int,
        user_id: int,
        payload: DebtUpdate,
    ) -> Debt:
        """Update a debt, optionally linking it to a transaction."""
        debt = await self.get_debt_by_id(debt_repository, debt_id, user_id)

        # Validate transaction if provided
        if payload.transaction_id is not None:
            transaction = await transaction_repository.get_by_id(payload.transaction_id)
            if not transaction:
                raise NotFoundException(
                    f"Movimiento con ID {payload.transaction_id} no encontrado")
            if transaction.user_id != user_id:
                raise ForbiddenException(
                    "El movimiento no pertenece al usuario")
            debt.transaction_id = payload.transaction_id

        # Update only provided fields
        if payload.type is not None:
            debt.type = payload.type
        if payload.person_name is not None:
            debt.person_name = payload.person_name
        if payload.amount is not None:
            debt.amount = payload.amount
        if payload.date is not None:
            debt.date = payload.date
        if payload.status is not None:
            debt.status = payload.status
        if payload.note is not None:
            debt.note = payload.note

        await debt_repository.update(debt)
        await debt_repository.commit()

        return debt

    async def delete_debt(
        self,
        debt_repository: DebtRepository,
        debt_id: int,
        user_id: int,
    ) -> None:
        """Delete a debt."""
        debt = await self.get_debt_by_id(debt_repository, debt_id, user_id)

        await debt_repository.delete(debt)
        await debt_repository.commit()
