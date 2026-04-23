from __future__ import annotations

from datetime import datetime

from sqlalchemy import func, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.entities.user.model import User
    from src.entities.transaction.model import Transaction

from src.utils.connection_db import Model
from src.utils.enums import AccountTypeEnum


class Account(Model):
    """
    Entidad de cuenta financiera.

    Representa una cuenta de usuario (banco, efectivo, digital, etc.)
    con su saldo correspondiente.
    """
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[AccountTypeEnum] = mapped_column(
        Enum(AccountTypeEnum, name="account_type_enum"),
        nullable=True
    )
    balance: Mapped[float] = mapped_column(default=0.0)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # Relaciones (usar referencias de string para evitar importes circulares)
    user: Mapped["User"] = relationship(
        "User", back_populates="accounts")
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="account", cascade="all, delete-orphan"
    )
