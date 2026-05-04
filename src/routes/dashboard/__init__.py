from fastapi import APIRouter

from src.exceptions import docs
from .controller import DashboardController
from .responses import DashboardSummaryResponse

dashboard_router: APIRouter = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
    responses={
        401: {"model": docs.UnAuthorizedException},
        403: {"model": docs.ForbiddenException},
        404: {"model": docs.NotFoundException},
    },
)

controller = DashboardController()

dashboard_router.add_api_route(
    "/summary",
    controller.get_summary,
    methods=["GET"],
    response_model=DashboardSummaryResponse,
    summary="Get dashboard summary",
    description="Obtiene un resumen del dashboard con ingresos, gastos, balance y movimientos recientes para el mes/año especificado.",
)
