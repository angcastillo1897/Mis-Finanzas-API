from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.users.models import User
from app.shared.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repositorio de usuarios."""

    def __init__(self, session: AsyncSession) -> None:
        """Inicializa el repositorio de usuarios.

        Args:
            session: Sesión de base de datos.
        """
        super().__init__(User, session)

    async def get_by_email(self, email: str) -> User | None:
        """Obtiene un usuario por su email.

        Args:
            email: Email del usuario.

        Returns:
            Usuario encontrado o None.
        """
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
