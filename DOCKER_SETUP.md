# Docker PostgreSQL Setup

## Quick Start

Esta guía te ayudará a configurar una base de datos PostgreSQL local usando Docker Compose para desarrollo.

### Requisitos

- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/install/) (incluido con Docker Desktop en Windows y Mac)

### Uso

#### 1. Iniciar el contenedor de PostgreSQL

```bash
docker-compose up -d
```

Este comando:

- Inicia un contenedor PostgreSQL en background (`-d` flag)
- Crea la base de datos `misfinanzas_db` automáticamente
- Mapea el puerto 5432 del contenedor al puerto 5432 de tu máquina
- Crea un volumen `postgres_data` para persistencia de datos

#### 2. Verificar que la BD está lista

```bash
docker-compose ps
```

Deberías ver algo como:

```
NAME              COMMAND                  SERVICE             STATUS
misfinanzas_db    "docker-entrypoint.s…"   postgres            Up 2 seconds (healthy)
```

#### 3. Conectar con la aplicación

Tu `.env` debe tener:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/misfinanzas_db
```

Luego corre tu aplicación normalmente:

```bash
uv run uvicorn app.main:app --reload
```

### Comandos útiles

**Ver logs del contenedor:**

```bash
docker-compose logs postgres
```

**Ver logs en tiempo real:**

```bash
docker-compose logs -f postgres
```

**Detener el contenedor (mantiene los datos):**

```bash
docker-compose stop
```

**Reiniciar el contenedor:**

```bash
docker-compose restart
```

**Eliminar el contenedor (mantiene los datos en el volumen):**

```bash
docker-compose down
```

**Eliminar completamente (incluyendo volumen de datos):**

```bash
docker-compose down -v
```

### Conectarse a la BD directamente

Puedes usar `psql` o herramientas como DBeaver, pgAdmin, etc.

**Con psql (si lo tienes instalado):**

```bash
psql -h localhost -U user -d misfinanzas_db
# Contraseña: password
```

**Con Docker:**

```bash
docker-compose exec postgres psql -U user -d misfinanzas_db
```

### Configuración de credenciales

Si necesitas cambiar las credenciales, edita el archivo `docker-compose.yml`:

```yaml
environment:
    POSTGRES_USER: tu_usuario # Cambiar aquí
    POSTGRES_PASSWORD: tu_contraseña # Cambiar aquí
    POSTGRES_DB: misfinanzas_db # Nombre de la BD
```

Y actualiza tu `.env` en consecuencia:

```env
DATABASE_URL=postgresql+asyncpg://tu_usuario:tu_contraseña@localhost:5432/misfinanzas_db
```

### Troubleshooting

**Error: "port 5432 already in use"**

- Cambiar el puerto en `docker-compose.yml`:
    ```yaml
    ports:
        - "5433:5432" # Usa puerto 5433 en tu máquina
    ```
- Actualizar `DATABASE_URL` en `.env`:
    ```env
    DATABASE_URL=postgresql+asyncpg://user:password@localhost:5433/misfinanzas_db
    ```

**La BD no se inicia**

- Revisar logs:
    ```bash
    docker-compose logs postgres
    ```

**Necesito limpiar todo y empezar de cero**

```bash
docker-compose down -v
docker-compose up -d
```

---

Para más información sobre Docker Compose: https://docs.docker.com/compose/
