from datetime import datetime

from pydantic import ConfigDict, EmailStr
from src.entities import SerializerModel


class UserSerializer(SerializerModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    first_name: str
    last_name: str
    created_at: datetime
