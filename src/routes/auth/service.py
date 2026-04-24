from src.entities.user.model import User
from src.entities.user.repository import UserRepository
from src.entities.user.schemas import UserCreate, UserLogin
from src.exceptions.bad_request import BadRequestException
from src.exceptions.unauthorized import UnAuthorizedException
from src.utils.security import create_access_token, hash_password, verify_password


class Service:
    async def register(
        self,
        user_repository: UserRepository,
        payload: UserCreate,
    ):
        existing = await user_repository.get_by_email(payload.email)
        if existing:
            raise BadRequestException("El email ya está registrado")

        new_user = User(
            email=payload.email,
            first_name=payload.first_name,
            last_name=payload.last_name,
            password_hash=hash_password(payload.password),
        )

        await user_repository.create(new_user)
        await user_repository.commit()

        token = create_access_token(str(new_user.id))
        return new_user, token

    async def login(
        self,
        user_repository: UserRepository,
        payload: UserLogin,
    ):
        user = await user_repository.get_by_email(payload.email)

        if not user or not verify_password(payload.password, user.password_hash):
            raise UnAuthorizedException("Credenciales inválidas")

        token = create_access_token(str(user.id))
        return user, token
