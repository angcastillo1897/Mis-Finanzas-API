from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.dependencies.async_db import AsyncSessionDepends
from src.entities.user.repository import UserRepository
from src.entities.user.model import User
from src.exceptions.unauthorized import UnAuthorizedException
from src.utils.security import get_subject_from_token

http_bearer = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(http_bearer),
    ],
    async_session: AsyncSessionDepends,
) -> User:
    if credentials is None or not credentials.credentials:
        raise UnAuthorizedException("Token requerido")

    token = credentials.credentials

    try:
        subject = get_subject_from_token(token)
        user_id = int(subject)
    except ValueError as exc:
        raise UnAuthorizedException("Token inválido o expirado") from exc

    user_repository = UserRepository(async_session)
    user = await user_repository.get_by_id(user_id)

    if not user:
        raise UnAuthorizedException("Usuario no autorizado")

    return user


CurrentUserDepends = Annotated[User, Depends(get_current_user)]
