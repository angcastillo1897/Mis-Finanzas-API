from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.exceptions import AppError, app_error_handler
from app.features.users.router import router as users_router
from app.features.users.exceptions import EmailAlreadyExistsError, UserNotFoundError


def create_app() -> FastAPI:
    """Crea y configura la aplicación FastAPI.

    Returns:
        FastAPI: Instancia de la aplicación configurada.
    """
    app = FastAPI(
        title="MisFinanzas API",
        description="API REST para gestión de finanzas personales",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"] if settings.is_development else [],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Registrar exception handlers
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(UserNotFoundError, user_not_found_handler)
    app.add_exception_handler(EmailAlreadyExistsError, email_already_exists_handler)

    # Registrar routers
    app.include_router(users_router)

    # Health check endpoint
    @app.get(
        "/health",
        tags=["health"],
        summary="Health check",
        description="Verifica que la API está operativa.",
    )
    async def health_check() -> dict[str, str]:
        """Endpoint de health check."""
        return {"status": "ok"}

    return app


async def user_not_found_handler(request: Request, exc: UserNotFoundError) -> JSONResponse:
    """Handler para UserNotFoundError.

    Args:
        request: Request object.
        exc: Excepción UserNotFoundError.

    Returns:
        JSONResponse con status 404.
    """
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc), "code": "USER_NOT_FOUND"},
    )


async def email_already_exists_handler(
    request: Request, exc: EmailAlreadyExistsError
) -> JSONResponse:
    """Handler para EmailAlreadyExistsError.

    Args:
        request: Request object.
        exc: Excepción EmailAlreadyExistsError.

    Returns:
        JSONResponse con status 409.
    """
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc), "code": "EMAIL_ALREADY_EXISTS"},
    )


app = create_app()
