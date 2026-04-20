from uuid import UUID

from app.core.exceptions import AppError


class UserNotFoundError(AppError):
    """Excepción cuando un usuario no es encontrado."""

    def __init__(self, user_id: UUID) -> None:
        super().__init__(f"User {user_id} not found")
        self.user_id = user_id


class EmailAlreadyExistsError(AppError):
    """Excepción cuando un email ya está registrado."""

    def __init__(self, email: str) -> None:
        super().__init__(f"Email {email} is already registered")
        self.email = email


class InvalidPasswordError(AppError):
    """Excepción cuando la contraseña es inválida."""

    def __init__(self) -> None:
        super().__init__("Invalid password")
