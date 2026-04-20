from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    """Schema para crear un usuario."""

    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    password: str
    full_name: str | None = None


class UserUpdate(BaseModel):
    """Schema para actualizar un usuario."""

    model_config = ConfigDict(extra="forbid")

    full_name: str | None = None


class UserRead(BaseModel):
    """Schema de respuesta para un usuario."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    full_name: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
