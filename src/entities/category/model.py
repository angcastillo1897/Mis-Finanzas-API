from __future__ import annotations

from datetime import datetime

from sqlalchemy import Enum, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.entities.transaction.model import Transaction
    from src.entities.user import User
from src.utils.connection_db import Model
from src.utils.enums import TransactionTypeEnum


class Category(Model):
    """
    Entidad de categoría.

    Representa las categorías de ingreso o gasto que el usuario puede usar
    para clasificar sus movimientos. Puede ser global o específica del usuario.
    """
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True, index=True
    )
    name: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[TransactionTypeEnum] = mapped_column(
        Enum(TransactionTypeEnum, name="transaction_type_enum"),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # Relaciones (usar referencias de string para evitar importes circulares)
    user: Mapped["User | None"] = relationship(
        "User", back_populates="categories")
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="category", cascade="all, delete-orphan"
    )
