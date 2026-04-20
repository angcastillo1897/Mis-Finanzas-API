# MisFinanzas API

API REST para gestión de finanzas personales construida con FastAPI, SQLAlchemy y Pydantic.

## Stack Tecnológico

- **FastAPI** - Framework HTTP async moderno
- **SQLAlchemy 2.x** - ORM con soporte async/await
- **Pydantic v2** - Validación y serialización de datos
- **PostgreSQL** - Base de datos
- **asyncpg** - Driver PostgreSQL async
- **Alembic** - Migraciones de BD
- **uv** - Gestor de paquetes y entornos virtuales

## Requisitos Previos

- Python 3.12+
- PostgreSQL 12+
- uv (gestor de paquetes)

## Instalación y Setup

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd MisFinanzasApi
```

### 2. Crear archivo .env

```bash
cp .env.example .env
```

Editar `.env` con tus valores:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/misfinanzas_db
SECRET_KEY=your-secret-key-here-min-32-chars
ENVIRONMENT=development
ACCESS_TOKEN_EXPIRE_MINUTES=30
LOG_LEVEL=INFO
```

### 3. Instalar dependencias

```bash
uv sync
```

### 4. Crear base de datos

```bash
# Crear la BD (si es necesario)
createdb misfinanzas_db
```

### 5. Aplicar migraciones

```bash
uv run alembic upgrade head
```

### 6. Ejecutar servidor de desarrollo

```bash
uv run uvicorn app.main:app --reload
```

La API estará disponible en `http://localhost:8000`

- Documentación Swagger: `http://localhost:8000/docs`
- Documentación ReDoc: `http://localhost:8000/redoc`

## Estructura del Proyecto

```
app/
├── core/                    # Configuración y seguridad
│   ├── config.py            # Settings de la aplicación
│   ├── security.py          # JWT, password hashing
│   └── exceptions.py        # Excepciones globales
│
├── db/
│   └── session.py           # Engine async, SessionLocal, get_db
│
├── shared/                  # Código compartido entre features
│   ├── models/
│   │   └── base.py          # Base ORM con TimestampMixin
│   ├── base_repository.py   # Repositorio genérico CRUD
│   └── pagination.py        # Schemas de paginación
│
├── features/                # Módulos de dominio (vertical slices)
│   └── users/
│       ├── models.py        # Entidad User
│       ├── schemas.py       # DTOs Pydantic
│       ├── exceptions.py    # Excepciones de dominio
│       ├── repository.py    # Acceso a datos
│       ├── service.py       # Lógica de negocio
│       ├── dependencies.py  # Inyección de deps
│       └── router.py        # Endpoints HTTP
│
├── main.py                  # App factory y registro
└── alembic/                 # Migraciones de BD
```

## Comandos Útiles

### Desarrollo

```bash
# Ejecutar servidor con hot reload
uv run uvicorn app.main:app --reload

# Lint y formateo
uv run ruff check .
uv run ruff format .

# Type checking
uv run mypy app

# Tests
uv run pytest tests
```

### Base de Datos

```bash
# Crear nueva migración
uv run alembic revision --autogenerate -m "descripción"

# Aplicar migraciones
uv run alembic upgrade head

# Revertir última migración
uv run alembic downgrade -1

# Ver estado de migraciones
uv run alembic current
```

## Endpoints Disponibles

### Users

- `POST /users/` - Registrar usuario
- `GET /users/` - Listar usuarios (paginado)
- `GET /users/{user_id}` - Obtener usuario por ID
- `PATCH /users/{user_id}` - Actualizar usuario
- `DELETE /users/{user_id}` - Eliminar usuario

## Convenciones

Ver el archivo `AGENTS.md` para:

- Estructura de proyecto
- Convenciones de código
- Patrones de arquitectura
- Mejores prácticas

## Licencia

MIT

## Autor

MisFinanzas Team
