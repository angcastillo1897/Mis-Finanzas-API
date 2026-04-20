from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# Configurar contexto de hashing para passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hashea un password con bcrypt.

    Args:
        password: Password en texto plano.

    Returns:
        Password hasheado.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica un password contra su hash.

    Args:
        plain_password: Password en texto plano.
        hashed_password: Password hasheado.

    Returns:
        True si el password es válido, False en caso contrario.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """Crea un JWT access token.

    Args:
        data: Datos a incluir en el token.
        expires_delta: Duración personalizada del token. Si es None, usa la configuración.

    Returns:
        JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def verify_token(token: str) -> dict[str, Any] | None:
    """Verifica y decodifica un JWT token.

    Args:
        token: JWT token a verificar.

    Returns:
        Datos del token si es válido, None en caso contrario.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        return None
