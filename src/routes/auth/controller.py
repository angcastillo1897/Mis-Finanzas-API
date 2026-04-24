from src.dependencies.async_db import AsyncSessionDepends
from src.dependencies.auth import CurrentUserDepends
from src.entities.user.repository import UserRepository
from src.entities.user.serializer import UserSerializer
from src.routes.auth.requests import LoginRequest, RegisterRequest
from src.routes.auth.responses import (
    AuthLoginResponse,
    AuthMeResponse,
    AuthRegisterResponse,
)
from src.routes.auth.service import Service


class Controller:
    def __init__(self) -> None:
        self.service = Service()

    async def register(
        self,
        payload: RegisterRequest,
        async_session: AsyncSessionDepends,
    ) -> AuthRegisterResponse:
        user, token = await self.service.register(
            UserRepository(async_session),
            payload,
        )
        return AuthRegisterResponse(
            access_token=token,
            user=UserSerializer.model_validate(user),
        )

    async def login(
        self,
        payload: LoginRequest,
        async_session: AsyncSessionDepends,
    ) -> AuthLoginResponse:
        user, token = await self.service.login(
            UserRepository(async_session),
            payload,
        )
        return AuthLoginResponse(
            access_token=token,
            user=UserSerializer.model_validate(user),
        )

    async def me(self, user: CurrentUserDepends) -> AuthMeResponse:
        return AuthMeResponse(user=UserSerializer.model_validate(user))
