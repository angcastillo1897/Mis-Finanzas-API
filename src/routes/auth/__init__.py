from fastapi import APIRouter

from src.exceptions import docs

from .controller import Controller
from .responses import AuthLoginResponse, AuthMeResponse, AuthRegisterResponse

auth_router: APIRouter = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={
        401: {"model": docs.UnAuthorizedException},
    },
)

controller = Controller()

auth_router.add_api_route(
    "/register",
    controller.register,
    methods=["POST"],
    response_model=AuthRegisterResponse,
    summary="Register",
    description="Registra un nuevo usuario y retorna su JWT.",
)

auth_router.add_api_route(
    "/login",
    controller.login,
    methods=["POST"],
    response_model=AuthLoginResponse,
    summary="Login",
    description="Autentica un usuario y retorna su JWT.",
)

auth_router.add_api_route(
    "/me",
    controller.me,
    methods=["GET"],
    response_model=AuthMeResponse,
    summary="Get current user",
    description="Retorna el usuario autenticado a partir del token bearer.",
)
