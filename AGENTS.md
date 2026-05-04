# MisFinanzas API - AI Agent Foundation (AGENTS.md)

This document outlines the architecture, coding standards, and data flows of the MisFinanzas API project. It serves as the primary context for AI agents (like Antigravity) to understand how to correctly generate, modify, and structure code within this codebase.

## 1. Architectural Layers & Project Structure

The project follows a modular, domain-driven architecture. Instead of separating files purely by technical function (e.g., all models together, all controllers together), the codebase is organized by **Features/Entities** and divided into two main macro-domains: `entities` (Core Domain) and `routes` (Delivery & Application Logic).

### Directory Structure

- **`src/entities/{domain}/`**: Contains the core domain definitions and data access.
  - `model.py`: SQLAlchemy ORM models. Must inherit from `src.utils.connection_db.Model`.
  - `repository.py`: Data access layer. Must inherit from `src.entities.RepositoryBase`. Handles all database queries using `AsyncSession`.
  - `schemas.py`: Pydantic models for **input validation** (e.g., `Create`, `Update`).
  - `serializer.py`: Pydantic models for **output serialization** (API responses). Uses `model_config = ConfigDict(from_attributes=True)`.

- **`src/routes/{domain}/`**: Contains the HTTP delivery mechanism and business logic.
  - `__init__.py`: FastAPI `APIRouter` definition. Defines the endpoints, methods, and OpenAPI documentation, mapping them to Controller methods.
  - `controller.py`: Receives HTTP requests, injects dependencies (User, Session), instantiates the Repository, calls the Service, and formats the response.
  - `service.py`: Core business logic. Validates permissions, enforces business rules, raises custom exceptions, and orchestrates the Repository.
  - `requests.py`: API-specific request definitions that extend from `entities/{domain}/schemas.py`.
  - `responses.py`: API-specific response definitions that wrap the serializer in a `data` field (e.g., `data: AccountSerializer`).

- **`src/dependencies/`**: FastAPI injectables (e.g., `AsyncSessionDepends`, `CurrentUserDepends`).
- **`src/exceptions/`**: Custom domain exceptions (e.g., `NotFoundException`, `ForbiddenException`). Handled globally in `main.py`.
- **`src/utils/`**: Shared utilities, Enums, and database configuration.

## 2. Request / Response Flow (The "Flow")

Every new endpoint should strictly follow this linear flow:

1. **Route (`__init__.py`)**: Receives the HTTP request and delegates it to the Controller.
2. **Controller (`controller.py`)**:
   - Injects the Current User (`CurrentUserDepends`) and DB Session (`AsyncSessionDepends`).
   - Instantiates the `Repository` with the session.
   - Calls the appropriate method in the `Service`.
   - Wraps the returned domain entity in the corresponding `Response` model (from `responses.py`).
3. **Service (`service.py`)**:
   - Executes business rules.
   - **Critical**: Verifies resource ownership and permissions (e.g., `if account.user_id != user_id: raise ForbiddenException(...)`).
   - Calls the `Repository` for CRUD operations.
   - Explicitly calls `await repository.commit()` after state-changing operations (Create, Update, Delete).
4. **Repository (`repository.py`)**:
   - Executes SQLAlchemy async queries (e.g., `execute`, `scalar_one_or_none`).
   - Uses `flush()` in operations like `create`, `update`, and `delete` to get IDs without committing the transaction.

## 3. Strict Coding Rules & Conventions

### Asynchronous Programming
- Use `async def` and `await` everywhere.
- Use `AsyncSession` for SQLAlchemy interactions.

### Dependency Injection
- Controllers must use FastAPI `Depends` to get the user and DB session.
- **Service Layer**: Do not instantiate repositories inside the Service. Instead, pass the repository instance from the Controller to the Service method. This makes the Service easily testable.

### Pydantic Models & Serialization
- Schemas and Serializers must inherit from `SerializerModel` (defined in `src.entities.__init__`), which automatically uses camelCase for JSON keys (`alias_generator=to_camel_case`).
- Keep input schemas (`schemas.py`) strictly separated from output serializers (`serializer.py`).

### API Responses
- All successful responses must be wrapped in a dictionary/object with a `data` key. 
  - *Example*: `{"data": {"id": 1, "name": "..."}}`
  - This is enforced by models in `responses.py` (e.g., `class AccountResponse(SerializerModel): data: AccountSerializer`).

### Database Transactions
- The `Repository` extends `RepositoryBase[T]`, which provides `commit`, `flush`, and `rollback`.
- Use `flush()` in repository methods (like `create`, `update`) to reflect changes in the session without committing.
- Call `commit()` explicitly from the **Service** layer once all business logic and multiple repository calls succeed.

### Error Handling
- Never return explicit HTTP 4xx/5xx responses from the Service or Controller.
- Instead, raise custom exceptions from `src.exceptions` (e.g., `NotFoundException`, `ForbiddenException`). These are automatically caught and transformed into appropriate HTTP responses by the global `exception_handlers`.

### Typing
- Fully type-hint all variables, arguments, and return types.
- Use new Python 3.10+ syntax: `| None` instead of `Optional`, and built-in generics like `list[T]` instead of `List[T]`.
