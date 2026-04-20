from fastapi import Request, status
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Excepción base para todos los errores de dominio de la aplicación."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message


class ValidationError(AppError):
    """Error de validación de datos."""

    pass


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    """Handler para excepciones AppError genéricas.

    Args:
        request: Request object.
        exc: Excepción AppError.

    Returns:
        JSONResponse con status 400 y detalle del error.
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc), "code": "VALIDATION_ERROR"},
    )
