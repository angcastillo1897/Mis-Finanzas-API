from fastapi import APIRouter

from src.exceptions import docs
from .controller import CategoryController
from .responses import CategoryResponse, CategoryListResponse

categories_router: APIRouter = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    responses={
        401: {"model": docs.UnAuthorizedException},
        403: {"model": docs.ForbiddenException},
        404: {"model": docs.NotFoundException},
    },
)

controller = CategoryController()

categories_router.add_api_route(
    "",
    controller.get_all_categories,
    methods=["GET"],
    response_model=CategoryListResponse,
    summary="Get all categories",
    description="Obtiene todas las categorías globales y del usuario autenticado, opcionalmente filtradas por tipo.",
)

categories_router.add_api_route(
    "",
    controller.create_category,
    methods=["POST"],
    response_model=CategoryResponse,
    summary="Create category",
    description="Crea una nueva categoría para el usuario autenticado.",
)

categories_router.add_api_route(
    "/{category_id}",
    controller.update_category,
    methods=["PUT"],
    response_model=CategoryResponse,
    summary="Update category",
    description="Actualiza una categoría existente del usuario autenticado.",
)

categories_router.add_api_route(
    "/{category_id}",
    controller.delete_category,
    methods=["DELETE"],
    summary="Delete category",
    description="Elimina una categoría del usuario autenticado.",
)
