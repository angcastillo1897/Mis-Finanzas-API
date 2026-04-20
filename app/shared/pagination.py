from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Parámetros de paginación para endpoints de listado."""

    page: int = 1
    size: int = 20

    @property
    def offset(self) -> int:
        """Calcula el offset basado en page y size."""
        return (self.page - 1) * self.size


class PagedResponse(BaseModel, Generic[T]):
    """Respuesta paginada genérica."""

    items: list[T]
    total: int
    page: int
    size: int

    @property
    def pages(self) -> int:
        """Calcula el número total de páginas."""
        return (self.total + self.size - 1) // self.size
