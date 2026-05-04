from fastapi import APIRouter

from src.exceptions import docs
from .controller import AccountController
from .responses import AccountResponse, AccountListResponse

accounts_router: APIRouter = APIRouter(
    prefix="/accounts",
    tags=["Accounts"],
    responses={
        401: {"model": docs.UnAuthorizedException},
        403: {"model": docs.ForbiddenException},
        404: {"model": docs.NotFoundException},
    },
)

controller = AccountController()

accounts_router.add_api_route(
    "",
    controller.get_all_accounts,
    methods=["GET"],
    response_model=AccountListResponse,
    summary="Get all accounts",
    description="Obtiene todas las cuentas del usuario autenticado.",
)

accounts_router.add_api_route(
    "",
    controller.create_account,
    methods=["POST"],
    response_model=AccountResponse,
    summary="Create account",
    description="Crea una nueva cuenta para el usuario autenticado.",
)

accounts_router.add_api_route(
    "/{account_id}",
    controller.update_account,
    methods=["PUT"],
    response_model=AccountResponse,
    summary="Update account",
    description="Actualiza una cuenta existente del usuario autenticado.",
)

accounts_router.add_api_route(
    "/{account_id}",
    controller.delete_account,
    methods=["DELETE"],
    summary="Delete account",
    description="Elimina una cuenta del usuario autenticado.",
)

accounts_router.add_api_route(
    "/{account_id}/recalculate-balance",
    controller.recalculate_account_balance,
    methods=["POST"],
    response_model=AccountResponse,
    summary="Recalculate account balance",
    description="Recalcula el saldo de la cuenta desde todos los movimientos (para verificación de integridad de datos).",
)
