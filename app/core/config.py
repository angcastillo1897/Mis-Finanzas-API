import logging
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la aplicación desde variables de entorno."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    @property
    def is_production(self) -> bool:
        """Verifica si el ambiente es producción."""
        return self.ENVIRONMENT == "production"

    @property
    def is_development(self) -> bool:
        """Verifica si el ambiente es desarrollo."""
        return self.ENVIRONMENT == "development"


settings = Settings()

# Configurar logging
logger = logging.getLogger("app")
logger.setLevel(settings.LOG_LEVEL)
