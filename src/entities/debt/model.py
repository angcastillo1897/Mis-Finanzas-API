from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import func, Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.entities.user.model import User
    from src.entities.transaction.model import Transaction
from src.utils.connection_db import Model
from src.utils.enums import DebtTypeEnum, DebtStatusEnum


class Debt(Model):
    """
    Entidad de deuda.

    Representa deudas personales (dinero que debo o me deben).
    Opcionalmente puede estar vinculada a un movimiento financiero.
    """
    __tablename__ = "debts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True)
    type: Mapped[DebtTypeEnum] = mapped_column(
        Enum(DebtTypeEnum, name="debt_type_enum"),
        nullable=False
    )
    person_name: Mapped[str] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    date: Mapped[date] = mapped_column(nullable=False)
    status: Mapped[DebtStatusEnum] = mapped_column(
        Enum(DebtStatusEnum, name="debt_status_enum"),
        nullable=False
    )
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    transaction_id: Mapped[int | None] = mapped_column(
        ForeignKey("transactions.id"), nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # Relaciones (usar referencias de string para evitar importes circulares)
    user: Mapped["User"] = relationship("User", back_populates="debts")
    transaction: Mapped["Transaction | None"] = relationship(
        "Transaction", back_populates="debts")
