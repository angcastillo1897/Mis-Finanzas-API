from fastapi import APIRouter

from src.exceptions import docs
from .controller import DebtController
from .responses import DebtResponse, DebtListResponse

debts_router: APIRouter = APIRouter(
    prefix="/debts",
    tags=["Debts"],
    responses={
        401: {"model": docs.UnAuthorizedException},
        403: {"model": docs.ForbiddenException},
        404: {"model": docs.NotFoundException},
    },
)

controller = DebtController()

debts_router.add_api_route(
    "",
    controller.get_all_debts,
    methods=["GET"],
    response_model=DebtListResponse,
    summary="Get all debts",
    description="Obtiene todas las deudas del usuario autenticado con filtros opcionales.",
)

debts_router.add_api_route(
    "/{debt_id}",
    controller.get_debt_by_id,
    methods=["GET"],
    response_model=DebtResponse,
    summary="Get debt",
    description="Obtiene una deuda específica del usuario autenticado.",
)

debts_router.add_api_route(
    "",
    controller.create_debt,
    methods=["POST"],
    response_model=DebtResponse,
    summary="Create debt",
    description="Crea una nueva deuda para el usuario autenticado (independiente de movimientos).",
)

debts_router.add_api_route(
    "/{debt_id}",
    controller.update_debt,
    methods=["PUT"],
    response_model=DebtResponse,
    summary="Update debt",
    description="Actualiza una deuda existente y opcionalmente la vincula a un movimiento cuando se paga.",
)

debts_router.add_api_route(
    "/{debt_id}",
    controller.delete_debt,
    methods=["DELETE"],
    summary="Delete debt",
    description="Elimina una deuda del usuario autenticado.",
)
