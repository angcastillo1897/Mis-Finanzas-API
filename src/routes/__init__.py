from fastapi import FastAPI

from .auth import auth_router
from .accounts import accounts_router
from .categories import categories_router
from .movements import movements_router
from .debts import debts_router
from .dashboard import dashboard_router

from src.settings import setting


def load_routes(app: FastAPI) -> None:
    app.include_router(auth_router, prefix=setting.API_PREFIX)
    app.include_router(accounts_router, prefix=setting.API_PREFIX)
    app.include_router(categories_router, prefix=setting.API_PREFIX)
    app.include_router(movements_router, prefix=setting.API_PREFIX)
    app.include_router(debts_router, prefix=setting.API_PREFIX)
    app.include_router(dashboard_router, prefix=setting.API_PREFIX)
