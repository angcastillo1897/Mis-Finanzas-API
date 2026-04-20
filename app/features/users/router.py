from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.features.users.dependencies import get_user_service
from app.features.users.schemas import UserCreate, UserRead, UserUpdate
from app.features.users.service import UserService
from app.shared.pagination import PagedResponse, PaginationParams

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar usuario",
    description="Crea un nuevo usuario. Devuelve 409 si el email ya está registrado.",
)
async def register_user(
    data: UserCreate,
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserRead:
    """Registra un nuevo usuario en la plataforma."""
    return await service.register(data)


@router.get(
    "/",
    response_model=PagedResponse[UserRead],
    summary="Listar usuarios",
    description="Obtiene todos los usuarios con soporte de paginación.",
)
async def list_users(
    page: int = 1,
    size: int = 20,
    service: Annotated[UserService, Depends(get_user_service)] = None,
) -> PagedResponse[UserRead]:
    """Lista todos los usuarios disponibles."""
    users, total = await service.get_all(page=page, size=size)
    return PagedResponse(
        items=users,
        total=total,
        page=page,
        size=size,
    )


@router.get(
    "/{user_id}",
    response_model=UserRead,
    summary="Obtener usuario por ID",
    description="Obtiene los detalles de un usuario específico.",
)
async def get_user(
    user_id: UUID,
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserRead:
    """Obtiene los detalles de un usuario por su ID."""
    return await service.get_or_raise(user_id)


@router.patch(
    "/{user_id}",
    response_model=UserRead,
    summary="Actualizar usuario",
    description="Actualiza los datos de un usuario existente.",
)
async def update_user(
    user_id: UUID,
    data: UserUpdate,
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserRead:
    """Actualiza los datos de un usuario."""
    return await service.update_user(user_id, data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="Elimina un usuario de la plataforma.",
)
async def delete_user(
    user_id: UUID,
    service: Annotated[UserService, Depends(get_user_service)],
) -> None:
    """Elimina un usuario de la plataforma."""
    await service.delete_user(user_id)
