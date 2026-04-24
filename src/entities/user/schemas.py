from pydantic import EmailStr, Field

from src.entities import SerializerModel


class UserCreate(SerializerModel):
    email: EmailStr
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=8, max_length=128)


class UserLogin(SerializerModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
