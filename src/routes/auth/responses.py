
from src.entities.user.serializer import UserSerializer
from src.entities import SerializerModel


class AuthTokenResponse(SerializerModel):
    access_token: str
    token_type: str = "bearer"


class AuthLoginResponse(AuthTokenResponse):
    user: UserSerializer


class AuthRegisterResponse(AuthTokenResponse):
    user: UserSerializer


class AuthMeResponse(SerializerModel):
    user: UserSerializer
