from datetime import date

from src.entities.transaction.model import Transaction
from src.entities.transaction.repository import TransactionRepository
from src.entities.transaction.schemas import TransactionCreate, TransactionUpdate
from src.entities.account.repository import AccountRepository
from src.entities.category.repository import CategoryRepository
from src.exceptions.not_found import NotFoundException
from src.exceptions.forbidden_exception import ForbiddenException
from src.utils.enums import TransactionTypeEnum


class MovementService:
    async def get_all_movements(
        self,
        transaction_repository: TransactionRepository,
        user_id: int,
        movement_type: str | None = None,
        category_id: int | None = None,
        account_id: int | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[Transaction]:
        """Get all movements for a user with optional filters."""
        # Parse type if provided
        parsed_type = None
        if movement_type:
            try:
                parsed_type = TransactionTypeEnum(movement_type)
            except ValueError:
                raise ValueError(
                    f"Tipo de movimiento inválido: {movement_type}")

        movements = await transaction_repository.get_all_for_user(
            user_id,
            parsed_type,
            category_id,
            account_id,
            from_date,
            to_date,
        )
        return movements

    async def get_movement_by_id(
        self,
        transaction_repository: TransactionRepository,
        movement_id: int,
        user_id: int,
    ) -> Transaction:
        """Get a specific movement, validating ownership."""
        movement = await transaction_repository.get_by_id(movement_id)

        if not movement:
            raise NotFoundException(
                f"Movimiento con ID {movement_id} no encontrado")

        if movement.user_id != user_id:
            raise ForbiddenException(
                "No tienes permiso para acceder este movimiento")

        return movement

    async def create_movement(
        self,
        transaction_repository: TransactionRepository,
        account_repository: AccountRepository,
        category_repository: CategoryRepository,
        user_id: int,
        payload: TransactionCreate,
    ) -> Transaction:
        """Create a new movement, validating account and category ownership, and updating balance."""
        # Validate account belongs to user
        account = await account_repository.get_by_id(payload.account_id)
        if not account or account.user_id != user_id:
            raise NotFoundException(
                "Cuenta no encontrada o no pertenece al usuario")

        # Validate category is accessible to user (global or user's own)
        category = await category_repository.get_by_id(payload.category_id)
        if not category:
            raise NotFoundException("Categoría no encontrada")
        if category.user_id is not None and category.user_id != user_id:
            raise ForbiddenException("Categoría no accesible")

        new_movement = Transaction(
            user_id=user_id,
            account_id=payload.account_id,
            category_id=payload.category_id,
            type=payload.type,
            amount=payload.amount,
            date=payload.date,
            note=payload.note,
        )

        # Create movement
        await transaction_repository.create(new_movement)

        # Update account balance based on transaction type
        is_income = payload.type == TransactionTypeEnum.INCOME
        await account_repository.update_balance(account, payload.amount, is_income)

        # Commit both operations atomically
        await transaction_repository.commit()

        return new_movement

    async def update_movement(
        self,
        transaction_repository: TransactionRepository,
        account_repository: AccountRepository,
        category_repository: CategoryRepository,
        movement_id: int,
        user_id: int,
        payload: TransactionUpdate,
    ) -> Transaction:
        """Update an existing movement, adjusting account balance accordingly."""
        movement = await self.get_movement_by_id(
            transaction_repository, movement_id, user_id
        )

        # Store original values for balance adjustment
        original_account_id = movement.account_id
        original_amount = movement.amount
        original_type = movement.type

        # Validate and update account if provided
        if payload.account_id is not None and payload.account_id != original_account_id:
            account = await account_repository.get_by_id(payload.account_id)
            if not account or account.user_id != user_id:
                raise NotFoundException(
                    "Cuenta no encontrada o no pertenece al usuario")
            movement.account_id = payload.account_id

        # Validate and update category if provided
        if payload.category_id is not None:
            category = await category_repository.get_by_id(payload.category_id)
            if not category:
                raise NotFoundException("Categoría no encontrada")
            if category.user_id is not None and category.user_id != user_id:
                raise ForbiddenException("Categoría no accesible")
            movement.category_id = payload.category_id

        # Update only provided fields
        if payload.type is not None:
            movement.type = payload.type
        if payload.amount is not None:
            movement.amount = payload.amount
        if payload.date is not None:
            movement.date = payload.date
        if payload.note is not None:
            movement.note = payload.note

        # Update movement in database
        await transaction_repository.update(movement)

        # Handle balance adjustments
        # First, reverse the original transaction effect
        original_account = await account_repository.get_by_id(original_account_id)
        if original_account:
            is_original_income = original_type == TransactionTypeEnum.INCOME
            if is_original_income:
                original_account.balance -= original_amount
            else:
                original_account.balance += original_amount
            await account_repository.update(original_account)

        # Then apply the new transaction effect
        new_account = await account_repository.get_by_id(movement.account_id)
        if new_account:
            is_new_income = movement.type == TransactionTypeEnum.INCOME
            await account_repository.update_balance(new_account, movement.amount, is_new_income)

        # Commit all balance changes atomically
        await transaction_repository.commit()

        return movement

    async def delete_movement(
        self,
        transaction_repository: TransactionRepository,
        account_repository: AccountRepository,
        movement_id: int,
        user_id: int,
    ) -> None:
        """Delete a movement, reversing the balance effect."""
        movement = await self.get_movement_by_id(
            transaction_repository, movement_id, user_id
        )

        # Get account to reverse balance
        account = await account_repository.get_by_id(movement.account_id)

        # Reverse the balance effect
        if account:
            is_income = movement.type == TransactionTypeEnum.INCOME
            if is_income:
                account.balance -= movement.amount
            else:
                account.balance += movement.amount
            await account_repository.update(account)

        # Delete the movement
        await transaction_repository.delete(movement)

        # Commit both operations atomically
        await transaction_repository.commit()
