# AGENTS.md — FastAPI REST API

Guía de convenciones, arquitectura y buenas prácticas para agentes de IA y desarrolladores que trabajen en este proyecto.

---

## Stack

| Herramienta                | Rol                                     |
| -------------------------- | --------------------------------------- |
| **FastAPI**                | Framework HTTP async                    |
| **SQLAlchemy 2.x (async)** | ORM con soporte nativo async/await      |
| **Pydantic v2**            | Validación, serialización, settings     |
| **uv**                     | Gestor de paquetes y entornos virtuales |
| **Alembic**                | Migraciones de base de datos            |
| **asyncpg**                | Driver PostgreSQL async                 |

---

## Estructura del proyecto

```
app/
├── features/                    # Módulos de dominio (vertical slices)
│   ├── users/
│   │   ├── __init__.py
│   │   ├── router.py            # Endpoints HTTP
│   │   ├── service.py           # Lógica de negocio
│   │   ├── repository.py        # Acceso a datos (ORM)
│   │   ├── schemas.py           # DTOs Pydantic (request / response)
│   │   ├── models.py            # Entidad ORM SQLAlchemy
│   │   ├── dependencies.py      # Deps FastAPI específicas del feature
│   │   └── exceptions.py        # Excepciones de dominio tipadas
│   ├── orders/
│   │   ├── models/              # Múltiples entidades → subcarpeta
│   │   │   ├── __init__.py      # Exporta Order, OrderItem, OrderStatus
│   │   │   ├── order.py
│   │   │   ├── order_item.py
│   │   │   └── order_status.py
│   │   └── ...
│   └── notifications/           # Feature sin entidad propia → sin models.py
│       ├── router.py
│       ├── service.py
│       └── schemas.py
│
├── shared/                      # Código genuinamente compartido entre features
│   ├── base_repository.py       # Repo genérico CRUD reutilizable
│   ├── pagination.py            # Schemas y utilidades de paginación
│   └── models/
│       ├── __init__.py
│       ├── base.py              # Base ORM: id UUID, created_at, updated_at
│       └── address.py           # Entidad compartida por 2+ features
│
├── core/
│   ├── config.py                # Settings con pydantic-settings + .env
│   ├── security.py              # JWT, password hashing
│   └── exceptions.py            # Exception handlers globales registrados en main
│
├── db/
│   └── session.py               # Engine async, SessionLocal, get_db dependency
│
├── main.py                      # App factory, routers, middlewares, handlers
├── alembic/
│   ├── env.py
│   └── versions/
├── tests/
│   ├── conftest.py
│   └── features/
│       └── users/
│           ├── test_router.py
│           ├── test_service.py
│           └── test_repository.py
├── pyproject.toml
└── .env.example
```

### Reglas de estructura

- Cada feature es un módulo autónomo. Puede tener cero, uno o varios `models`.
- Una entidad vive en el feature que **es su dueño** (quien define su ciclo de vida).
- Si una entidad la necesitan 2 o más features → se mueve a `shared/models/`.
- Un feature que necesita leer una entidad ajena importa desde el feature dueño. Nunca duplica.
- `shared/` solo crece cuando el código es utilizado por al menos dos features. No mover cosas ahí de forma anticipada.
- Features sin entidad propia (servicios de orquestación, notificaciones) simplemente no tienen `models.py`.

---

## Convenciones de código

### Generales

- Python 3.12+. Usar type hints en todas las funciones, sin excepción.
- Nunca usar `Any` de `typing` salvo casos extremadamente justificados con comentario.
- Imports absolutos siempre: `from app.features.users.models import User`, nunca relativos con `..`.
- Un archivo no debe superar las 300 líneas. Si lo supera, es señal de que necesita dividirse.
- No usar `print()` para debug. Usar `logging` con el logger configurado en `core/config.py`.
- Todas las funciones y clases públicas deben tener docstring en formato Google style.

### Nombrado

| Elemento               | Convención                                     | Ejemplo              |
| ---------------------- | ---------------------------------------------- | -------------------- |
| Variables / funciones  | `snake_case`                                   | `get_user_by_email`  |
| Clases                 | `PascalCase`                                   | `UserService`        |
| Constantes             | `UPPER_SNAKE_CASE`                             | `MAX_LOGIN_ATTEMPTS` |
| Archivos               | `snake_case.py`                                | `base_repository.py` |
| Schemas request        | `{Entity}Create`, `{Entity}Update`             | `UserCreate`         |
| Schemas response       | `{Entity}Read`, `{Entity}Summary`              | `UserRead`           |
| Excepciones de dominio | `{Entity}{Motivo}Error`                        | `UserNotFoundError`  |
| Endpoints              | verbos HTTP implícitos, sustantivos en la ruta | `GET /users/{id}`    |

---

## Capa por capa

### `models.py` — Entidades ORM

- Solo mapeo a base de datos. Cero lógica de negocio.
- Siempre heredar de `Base` en `shared/models/base.py` (incluye `id`, `created_at`, `updated_at`).
- Usar `UUID` como PK. Nunca autoincremental entero como PK expuesto en la API.
- Relaciones declaradas con `Mapped[]` y `mapped_column()` (SQLAlchemy 2.x style).
- No acceder a relaciones lazy fuera de la sesión. Usar `selectinload` o `joinedload` explícitamente en el repository.

```python
# app/features/users/models.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.shared.models.base import Base

class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    full_name: Mapped[str | None] = mapped_column(nullable=True)
```

### `schemas.py` — DTOs Pydantic

- Separar siempre `Create`, `Update`, `Read`. Nunca un schema único que sirva para todo.
- `Update` con todos los campos opcionales (`| None`). Usar `model_config` con `extra="forbid"` en los schemas de input.
- `Read` con `model_config = ConfigDict(from_attributes=True)` para serializar desde ORM.
- Nunca exponer `hashed_password`, campos internos ni timestamps de auditoría que el cliente no deba ver.
- Validaciones de negocio simples (formato de email, longitud) van en el schema. Validaciones que requieren DB (unicidad) van en el service.

```python
# app/features/users/schemas.py
from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr
    password: str
    full_name: str | None = None

class UserUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    full_name: str | None = None

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    email: EmailStr
    full_name: str | None
    is_active: bool
    created_at: datetime
```

### `exceptions.py` — Excepciones de dominio

- Todas las excepciones de dominio heredan de una base común del feature o de `AppError` en `core/exceptions.py`.
- **Nunca** lanzar `HTTPException` desde el service ni el repository. Solo desde el router o los exception handlers globales.
- Cada excepción lleva el contexto necesario para construir la respuesta HTTP en el handler.

```python
# app/features/users/exceptions.py
from app.core.exceptions import AppError

class UserNotFoundError(AppError):
    def __init__(self, user_id: UUID) -> None:
        super().__init__(f"User {user_id} not found")
        self.user_id = user_id

class EmailAlreadyExistsError(AppError):
    def __init__(self, email: str) -> None:
        super().__init__(f"Email {email} is already registered")
        self.email = email
```

```python
# app/core/exceptions.py  — handler global registrado en main.py
from fastapi import Request
from fastapi.responses import JSONResponse
from app.features.users.exceptions import UserNotFoundError, EmailAlreadyExistsError

async def user_not_found_handler(request: Request, exc: UserNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})

async def email_exists_handler(request: Request, exc: EmailAlreadyExistsError) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})
```

### `repository.py` — Acceso a datos

- Solo queries SQL/ORM. Sin lógica de negocio ni validaciones de dominio.
- Recibe la sesión como dependencia inyectada, nunca la instancia internamente.
- Métodos async siempre. Usar `await session.execute(select(...))`.
- Cargar relaciones explícitamente con `selectinload` cuando se necesiten. Nunca confiar en lazy loading.
- El repo base genérico en `shared/base_repository.py` provee `get`, `get_or_none`, `create`, `update`, `delete`, `list`. Extender solo cuando se necesite una query específica.

```python
# app/features/users/repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.shared.base_repository import BaseRepository
from app.features.users.models import User

class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
```

### `service.py` — Lógica de negocio

- Es la capa más importante. Aquí vive todo el "qué hace el sistema".
- No sabe nada de HTTP. No importa `Request`, `Response` ni `HTTPException`.
- No accede a la DB directamente. Solo habla con su repository (y opcionalmente con otros services).
- Orquesta: llama al repo, aplica reglas de negocio, lanza excepciones de dominio, coordina side effects (emails, eventos).
- Un método de service = un caso de uso. Si el método supera 25 líneas, considerar extraer un método privado auxiliar.
- Inyección por constructor. No usar estado mutable a nivel de instancia.

```python
# app/features/users/service.py
from uuid import UUID
from app.features.users.repository import UserRepository
from app.features.users.schemas import UserCreate, UserRead
from app.features.users.exceptions import UserNotFoundError, EmailAlreadyExistsError
from app.core.security import hash_password

class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    async def register(self, data: UserCreate) -> UserRead:
        """Registra un nuevo usuario. Lanza EmailAlreadyExistsError si el email ya existe."""
        existing = await self._repo.get_by_email(data.email)
        if existing:
            raise EmailAlreadyExistsError(data.email)

        user = await self._repo.create({
            "email": data.email,
            "hashed_password": hash_password(data.password),
            "full_name": data.full_name,
        })
        return UserRead.model_validate(user)

    async def get_or_raise(self, user_id: UUID) -> UserRead:
        """Obtiene un usuario por ID. Lanza UserNotFoundError si no existe."""
        user = await self._repo.get_or_none(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return UserRead.model_validate(user)
```

### `router.py` — Endpoints HTTP

- Es solo un adaptador HTTP → service. Sin lógica de negocio.
- Si un endpoint supera 10 líneas de lógica real (sin contar decoradores), algo está en el lugar equivocado.
- Usar siempre `response_model` explícito en cada endpoint.
- Documentar con `summary` y `description` en el decorador para un OpenAPI útil.
- Los status codes deben ser semánticamente correctos: `201` para creación, `204` para eliminación sin cuerpo.
- Nunca capturar excepciones de dominio en el router — los handlers globales lo hacen.

```python
# app/features/users/router.py
from uuid import UUID
from fastapi import APIRouter, Depends, status
from app.features.users.schemas import UserCreate, UserRead
from app.features.users.dependencies import get_user_service
from app.features.users.service import UserService

router = APIRouter()

@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar usuario",
    description="Crea un nuevo usuario. Devuelve 409 si el email ya está registrado.",
)
async def register_user(
    data: UserCreate,
    service: UserService = Depends(get_user_service),
) -> UserRead:
    return await service.register(data)

@router.get(
    "/{user_id}",
    response_model=UserRead,
    summary="Obtener usuario por ID",
)
async def get_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
) -> UserRead:
    return await service.get_or_raise(user_id)
```

### `dependencies.py` — Inyección de dependencias

- Centraliza la construcción del service y el repo para el feature.
- Usar `Annotated` para reusar deps sin repetir `Depends(...)`.
- La sesión de DB se inyecta aquí, no se instancia manualmente.

```python
# app/features/users/dependencies.py
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.features.users.repository import UserRepository
from app.features.users.service import UserService

def get_user_repository(session: Annotated[AsyncSession, Depends(get_db)]) -> UserRepository:
    return UserRepository(session)

def get_user_service(repo: Annotated[UserRepository, Depends(get_user_repository)]) -> UserService:
    return UserService(repo)
```

---

## Base ORM compartida

```python
# app/shared/models/base.py
import uuid
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class TimestampMixin:
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
```

---

## Configuración y settings

```python
# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

settings = Settings()
```

- Nunca hardcodear valores de configuración en el código.
- Nunca commitear `.env`. El repositorio debe incluir `.env.example` con todas las variables documentadas.
- Acceder a settings con `from app.core.config import settings`. No re-instanciar `Settings()`.

---

## Sesión de base de datos

```python
# app/db/session.py
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.ENVIRONMENT == "development",
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
```

- Siempre async. Nunca usar `Session` síncrona.
- `expire_on_commit=False` para poder acceder a atributos del ORM después del commit sin re-queries.
- La sesión se gestiona por request vía `Depends(get_db)`. Nunca como singleton global.

---

## Paginación

Todos los endpoints de listado deben soportar paginación. Usar el schema compartido:

```python
# app/shared/pagination.py
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class PaginationParams(BaseModel):
    page: int = 1
    size: int = 20

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

class PagedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    pages: int
```

---

## Respuestas de error

Todas las respuestas de error siguen el mismo contrato:

```json
{
    "detail": "Descripción del error legible para el cliente",
    "code": "USER_NOT_FOUND"
}
```

- `detail`: mensaje legible. Nunca exponer stack traces ni mensajes internos de SQLAlchemy.
- `code`: constante en UPPER_SNAKE_CASE para que el cliente pueda manejar casos específicos.
- Los handlers globales en `core/exceptions.py` mapean cada excepción de dominio a su status code HTTP.

---

## Comandos comunes (uv)

```bash
# Instalar dependencias
uv sync

# Agregar dependencia
uv add fastapi sqlalchemy asyncpg pydantic-settings

# Ejecutar servidor de desarrollo
uv run uvicorn app.main:app --reload

# Crear nueva migración
uv run alembic revision --autogenerate -m "add users table"

# Aplicar migraciones
uv run alembic upgrade head

# Revertir última migración
uv run alembic downgrade -1

# Lint y formato
uv run ruff check .
uv run ruff format .
```

---

## Migraciones con Alembic

- Cada migración modifica **una sola cosa** conceptual. No acumular cambios no relacionados.
- Siempre revisar el archivo generado por `--autogenerate` antes de aplicarlo. Alembic no detecta todo correctamente (renombrados, cambios de tipo en algunos dialectos).
- Las migraciones son código — se commitean y se revisan en PR.
- Nunca modificar una migración que ya fue aplicada en producción. Crear una nueva.
- El `env.py` de Alembic debe importar todos los modelos para que el autogenerate funcione:

```python
# alembic/env.py
from app.shared.models.base import Base
from app.features.users.models import User       # noqa: F401
from app.features.orders.models import Order     # noqa: F401
# ... importar todos los modelos aquí

target_metadata = Base.metadata
```

---

## Seguridad

- Nunca loguear passwords, tokens ni PII (emails, nombres) en producción.
- Usar `python-jose` o `PyJWT` para JWT. El secret key debe tener mínimo 32 caracteres aleatorios.
- Passwords hasheados con `bcrypt` a través de `passlib`. Nunca MD5, SHA1 ni almacenar en texto plano.
- CORS configurado explícitamente. En producción nunca `allow_origins=["*"]`.
- Rate limiting en endpoints de autenticación.
- Validar y sanitizar todos los inputs en los schemas Pydantic con `extra="forbid"`.

---

## Lo que un agente NUNCA debe hacer

- Poner lógica de negocio en el router.
- Poner queries SQL/ORM en el service.
- Lanzar `HTTPException` desde el service o el repository.
- Usar `session.execute()` en el service directamente.
- Importar una entidad ORM de un feature y usarla como si fuera de otro (siempre importar del dueño).
- Crear un `models.py` vacío o de relleno cuando el feature no tiene entidad propia.
- Mover código a `shared/` sin que lo usen al menos dos features.
- Commitear `.env` con valores reales.
- Usar `Any` sin justificación documentada.
- Exponer en la respuesta HTTP campos como `hashed_password`, IDs internos de audit, o mensajes de error de SQLAlchemy.
- Usar `session` fuera del scope de `get_db` (no guardar la sesión en una variable de módulo).
