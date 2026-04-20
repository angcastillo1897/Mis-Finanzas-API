from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.features.users.repository import UserRepository
from app.features.users.service import UserService


def get_user_repository(session: Annotated[AsyncSession, Depends(get_db)]) -> UserRepository:
    """Crea una instancia del repositorio de usuarios.

    Args:
        session: Sesión de base de datos inyectada.

    Returns:
        UserRepository: Instancia del repositorio.
    """
    return UserRepository(session)


def get_user_service(
    repo: Annotated[UserRepository, Depends(get_user_repository)]
) -> UserService:
    """Crea una instancia del servicio de usuarios.

    Args:
        repo: Repositorio de usuarios inyectado.

    Returns:
        UserService: Instancia del servicio.
    """
    return UserService(repo)
