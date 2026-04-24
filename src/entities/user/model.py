from __future__ import annotations

from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from src.entities.account.model import Account
from src.entities.transaction.model import Transaction
if TYPE_CHECKING:
    from src.entities.category.model import Category
    from src.entities.debt.model import Debt
from src.utils.connection_db import Model


class User(Model):
    """
    Entidad de usuario.

    Cada usuario representa una persona que usa la aplicación para gestionar sus finanzas.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # Relaciones (usar referencias de string para evitar importes circulares)
    accounts: Mapped[list["Account"]] = relationship(
        "Account", back_populates="user", cascade="all, delete-orphan"
    )
    categories: Mapped[list["Category"]] = relationship(
        "Category", back_populates="user", cascade="all, delete-orphan"
    )
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="user", cascade="all, delete-orphan"
    )
    debts: Mapped[list["Debt"]] = relationship(
        "Debt", back_populates="user", cascade="all, delete-orphan"
    )
