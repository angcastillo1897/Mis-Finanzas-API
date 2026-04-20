from uuid import UUID

from app.core.security import hash_password
from app.features.users.exceptions import EmailAlreadyExistsError, UserNotFoundError
from app.features.users.repository import UserRepository
from app.features.users.schemas import UserCreate, UserRead, UserUpdate


class UserService:
    """Servicio de lógica de negocio para usuarios."""

    def __init__(self, repo: UserRepository) -> None:
        """Inicializa el servicio de usuarios.

        Args:
            repo: Repositorio de usuarios.
        """
        self._repo = repo

    async def register(self, data: UserCreate) -> UserRead:
        """Registra un nuevo usuario. Lanza EmailAlreadyExistsError si el email ya existe.

        Args:
            data: Datos del nuevo usuario.

        Returns:
            Usuario creado.

        Raises:
            EmailAlreadyExistsError: Si el email ya está registrado.
        """
        existing = await self._repo.get_by_email(data.email)
        if existing:
            raise EmailAlreadyExistsError(data.email)

        user = await self._repo.create({
            "email": data.email,
            "hashed_password": hash_password(data.password),
            "full_name": data.full_name,
        })
        return UserRead.model_validate(user)

    async def get_or_raise(self, user_id: UUID) -> UserRead:
        """Obtiene un usuario por ID. Lanza UserNotFoundError si no existe.

        Args:
            user_id: ID del usuario.

        Returns:
            Usuario encontrado.

        Raises:
            UserNotFoundError: Si el usuario no existe.
        """
        user = await self._repo.get_or_none(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return UserRead.model_validate(user)

    async def get_all(self, page: int = 1, size: int = 20) -> tuple[list[UserRead], int]:
        """Obtiene todos los usuarios con paginación.

        Args:
            page: Número de página (1-indexed).
            size: Tamaño de página.

        Returns:
            Tupla de (lista de usuarios, total de usuarios).
        """
        skip = (page - 1) * size
        users = await self._repo.list(skip=skip, limit=size)
        total = await self._repo.count()
        return [UserRead.model_validate(u) for u in users], total

    async def update_user(self, user_id: UUID, data: UserUpdate) -> UserRead:
        """Actualiza un usuario.

        Args:
            user_id: ID del usuario.
            data: Datos a actualizar.

        Returns:
            Usuario actualizado.

        Raises:
            UserNotFoundError: Si el usuario no existe.
        """
        update_data = data.model_dump(exclude_unset=True)
        user = await self._repo.update(user_id, update_data)
        if not user:
            raise UserNotFoundError(user_id)
        return UserRead.model_validate(user)

    async def delete_user(self, user_id: UUID) -> None:
        """Elimina un usuario.

        Args:
            user_id: ID del usuario.

        Raises:
            UserNotFoundError: Si el usuario no existe.
        """
        deleted = await self._repo.delete(user_id)
        if not deleted:
            raise UserNotFoundError(user_id)
