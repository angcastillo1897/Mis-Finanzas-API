from fastapi import FastAPI

from .auth import auth_router

from src.settings import setting


def load_routes(app: FastAPI) -> None:
    app.include_router(auth_router, prefix=setting.API_PREFIX)
