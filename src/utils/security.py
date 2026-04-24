from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt  # type: ignore
from passlib.context import CryptContext  # type: ignore

from src.settings import setting

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, setting.SECRET_KEY, algorithm=setting.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, setting.SECRET_KEY, algorithms=[setting.JWT_ALGORITHM])


def get_subject_from_token(token: str) -> str:
    try:
        payload = decode_access_token(token)
        subject = payload.get("sub")
        if not subject or not isinstance(subject, str):
            raise ValueError("Token inválido")
        return subject
    except (JWTError, ValueError) as exc:
        raise ValueError("Token inválido") from exc
