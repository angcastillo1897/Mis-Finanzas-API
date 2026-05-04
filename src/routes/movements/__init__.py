from fastapi import APIRouter

from src.exceptions import docs
from .controller import MovementController
from .responses import MovementResponse, MovementListResponse

movements_router: APIRouter = APIRouter(
    prefix="/movements",
    tags=["Movements"],
    responses={
        401: {"model": docs.UnAuthorizedException},
        403: {"model": docs.ForbiddenException},
        404: {"model": docs.NotFoundException},
    },
)

controller = MovementController()

movements_router.add_api_route(
    "",
    controller.get_all_movements,
    methods=["GET"],
    response_model=MovementListResponse,
    summary="Get all movements",
    description="Obtiene todos los movimientos del usuario autenticado con filtros opcionales.",
)

movements_router.add_api_route(
    "/{movement_id}",
    controller.get_movement_by_id,
    methods=["GET"],
    response_model=MovementResponse,
    summary="Get movement",
    description="Obtiene un movimiento específico del usuario autenticado.",
)

movements_router.add_api_route(
    "",
    controller.create_movement,
    methods=["POST"],
    response_model=MovementResponse,
    summary="Create movement",
    description="Crea un nuevo movimiento para el usuario autenticado.",
)

movements_router.add_api_route(
    "/{movement_id}",
    controller.update_movement,
    methods=["PUT"],
    response_model=MovementResponse,
    summary="Update movement",
    description="Actualiza un movimiento existente del usuario autenticado.",
)

movements_router.add_api_route(
    "/{movement_id}",
    controller.delete_movement,
    methods=["DELETE"],
    summary="Delete movement",
    description="Elimina un movimiento del usuario autenticado.",
)
