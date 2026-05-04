from src.entities.category.model import Category
from src.entities.category.repository import CategoryRepository
from src.entities.category.schemas import CategoryCreate, CategoryUpdate
from src.exceptions.not_found import NotFoundException
from src.exceptions.forbidden_exception import ForbiddenException
from src.utils.enums import TransactionTypeEnum


class CategoryService:
    async def get_all_categories(
        self,
        category_repository: CategoryRepository,
        user_id: int,
        category_type: str | None = None,
    ) -> list[Category]:
        """Get all global and user-specific categories, optionally filtered by type."""
        # Parse category_type if provided
        parsed_type = None
        if category_type:
            try:
                parsed_type = TransactionTypeEnum(category_type)
            except ValueError:
                raise ValueError(
                    f"Tipo de categoría inválido: {category_type}")

        categories = await category_repository.get_all_for_user(user_id, parsed_type)
        return categories

    async def get_category_by_id(
        self,
        category_repository: CategoryRepository,
        category_id: int,
        user_id: int,
    ) -> Category:
        """Get a specific category, validating it's global or belongs to user."""
        category = await category_repository.get_by_id(category_id)

        if not category:
            raise NotFoundException(
                f"Categoría con ID {category_id} no encontrada")

        # Allow access if it's a global category OR user's own category
        if category.user_id is not None and category.user_id != user_id:
            raise ForbiddenException(
                "No tienes permiso para acceder esta categoría")

        return category

    async def create_category(
        self,
        category_repository: CategoryRepository,
        user_id: int,
        payload: CategoryCreate,
    ) -> Category:
        """Create a new category for the user."""
        new_category = Category(
            user_id=user_id,
            name=payload.name,
            type=payload.type,
        )

        await category_repository.create(new_category)
        await category_repository.commit()

        return new_category

    async def update_category(
        self,
        category_repository: CategoryRepository,
        category_id: int,
        user_id: int,
        payload: CategoryUpdate,
    ) -> Category:
        """Update a user-specific category."""
        category = await category_repository.get_by_id(category_id)

        if not category:
            raise NotFoundException(
                f"Categoría con ID {category_id} no encontrada")

        # Only allow updating user's own categories, not global ones
        if category.user_id != user_id:
            raise ForbiddenException(
                "No tienes permiso para modificar esta categoría")

        # Update only provided fields
        if payload.name is not None:
            category.name = payload.name
        if payload.type is not None:
            category.type = payload.type

        await category_repository.update(category)
        await category_repository.commit()

        return category

    async def delete_category(
        self,
        category_repository: CategoryRepository,
        category_id: int,
        user_id: int,
    ) -> None:
        """Delete a user-specific category."""
        category = await category_repository.get_by_id(category_id)

        if not category:
            raise NotFoundException(
                f"Categoría con ID {category_id} no encontrada")

        # Only allow deleting user's own categories, not global ones
        if category.user_id != user_id:
            raise ForbiddenException(
                "No tienes permiso para eliminar esta categoría")

        await category_repository.delete(category)
        await category_repository.commit()
