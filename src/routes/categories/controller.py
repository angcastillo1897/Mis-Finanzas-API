from fastapi import Query

from src.dependencies.async_db import AsyncSessionDepends
from src.dependencies.auth import CurrentUserDepends
from src.entities.category.repository import CategoryRepository
from src.entities.category.serializer import CategorySerializer
from src.entities.user.model import User
from src.routes.categories.requests import CreateCategoryRequest, UpdateCategoryRequest
from src.routes.categories.responses import CategoryResponse, CategoryListResponse
from src.routes.categories.service import CategoryService


class CategoryController:
    def __init__(self) -> None:
        self.service = CategoryService()

    async def get_all_categories(
        self,
        user: CurrentUserDepends,
        async_session: AsyncSessionDepends,
        type: str | None = Query(
            None, description="Filter by category type: ingreso or gasto"),
    ) -> CategoryListResponse:
        """Get all global and user-specific categories, optionally filtered by type."""
        categories = await self.service.get_all_categories(
            CategoryRepository(async_session),
            user.id,
            type,
        )
        return CategoryListResponse(
            data=[CategorySerializer.model_validate(
                category) for category in categories]
        )

    async def create_category(
        self,
        payload: CreateCategoryRequest,
        user: CurrentUserDepends,
        async_session: AsyncSessionDepends,
    ) -> CategoryResponse:
        """Create a new category for the current user."""
        category = await self.service.create_category(
            CategoryRepository(async_session),
            user.id,
            payload,
        )
        return CategoryResponse(
            data=CategorySerializer.model_validate(category)
        )

    async def update_category(
        self,
        category_id: int,
        payload: UpdateCategoryRequest,
        user: CurrentUserDepends,
        async_session: AsyncSessionDepends,
    ) -> CategoryResponse:
        """Update an existing category."""
        category = await self.service.update_category(
            CategoryRepository(async_session),
            category_id,
            user.id,
            payload,
        )
        return CategoryResponse(
            data=CategorySerializer.model_validate(category)
        )

    async def delete_category(
        self,
        category_id: int,
        user: CurrentUserDepends,
        async_session: AsyncSessionDepends,
    ) -> dict:
        """Delete a category."""
        await self.service.delete_category(
            CategoryRepository(async_session),
            category_id,
            user.id,
        )
        return {"message": "Categoría eliminada exitosamente"}
