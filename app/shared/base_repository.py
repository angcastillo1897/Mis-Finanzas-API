from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Repositorio genérico con operaciones CRUD básicas."""

    def __init__(self, model: type[T], session: AsyncSession) -> None:
        """Inicializa el repositorio.

        Args:
            model: Clase de modelo ORM.
            session: Sesión de base de datos.
        """
        self.model = model
        self.session = session

    async def get(self, id: UUID) -> T | None:
        """Obtiene una entidad por su ID.

        Args:
            id: UUID de la entidad.

        Returns:
            Entidad encontrada o None.
        """
        return await self.session.get(self.model, id)

    async def get_or_none(self, id: UUID) -> T | None:
        """Alias para get() - obtiene una entidad por su ID.

        Args:
            id: UUID de la entidad.

        Returns:
            Entidad encontrada o None.
        """
        return await self.get(id)

    async def create(self, data: dict) -> T:
        """Crea una nueva entidad.

        Args:
            data: Diccionario con los datos de la entidad.

        Returns:
            Entidad creada.
        """
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def update(self, id: UUID, data: dict) -> T | None:
        """Actualiza una entidad.

        Args:
            id: UUID de la entidad.
            data: Diccionario con los datos a actualizar.

        Returns:
            Entidad actualizada o None si no existe.
        """
        instance = await self.get(id)
        if not instance:
            return None
        for key, value in data.items():
            setattr(instance, key, value)
        await self.session.flush()
        return instance

    async def delete(self, id: UUID) -> bool:
        """Elimina una entidad.

        Args:
            id: UUID de la entidad.

        Returns:
            True si se eliminó, False si no existía.
        """
        instance = await self.get(id)
        if not instance:
            return False
        await self.session.delete(instance)
        await self.session.flush()
        return True

    async def list(self, skip: int = 0, limit: int = 20) -> list[T]:
        """Lista todas las entidades con paginación.

        Args:
            skip: Número de registros a saltar.
            limit: Número máximo de registros a devolver.

        Returns:
            Lista de entidades.
        """
        result = await self.session.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def count(self) -> int:
        """Cuenta el total de entidades.

        Returns:
            Número total de entidades.
        """
        result = await self.session.execute(select(func.count(self.model.id)))
        return result.scalar() or 0


def func(x):
    """Re-exportar func de SQLAlchemy para count."""
    from sqlalchemy import func as sql_func
    return sql_func(x)
