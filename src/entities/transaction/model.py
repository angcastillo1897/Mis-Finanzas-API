from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import func, Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.entities.account.model import Account
    from src.entities.user.model import User

from src.entities.debt.model import Debt
from src.entities.category.model import Category
from src.utils.connection_db import Model
from src.utils.enums import TransactionTypeEnum


class Transaction(Model):
    """
    Entidad de movimiento financiero.

    Representa un ingreso o gasto que afecta el saldo de una cuenta.
    Está asociado a un usuario, una cuenta y una categoría.
    """
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True)
    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id"), nullable=False, index=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=False, index=True)
    type: Mapped[TransactionTypeEnum] = mapped_column(
        Enum(TransactionTypeEnum, name="transaction_type_enum"),
        nullable=False
    )
    amount: Mapped[float] = mapped_column(nullable=False)
    date: Mapped[date] = mapped_column(nullable=False)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # Relaciones (usar referencias de string para evitar importes circulares)
    user: Mapped["User"] = relationship(
        "User", back_populates="transactions")
    account: Mapped["Account"] = relationship(
        "Account", back_populates="transactions")
    category: Mapped["Category"] = relationship(
        "Category", back_populates="transactions")
    debts: Mapped[list["Debt"]] = relationship(
        "Debt", back_populates="transaction", cascade="all, delete-orphan"
    )
