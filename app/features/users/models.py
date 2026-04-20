from sqlalchemy.orm import Mapped, mapped_column

from app.shared.models.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    """Modelo de usuario."""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    full_name: Mapped[str | None] = mapped_column(nullable=True)
