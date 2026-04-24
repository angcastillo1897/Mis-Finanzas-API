import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from src.exceptions import exception_handlers
from src.routes import load_routes
from src.settings import setting

app: FastAPI = FastAPI(
    title="Mis Finanzas API",
    description="API para la gestion de las finanzas personales",
    version="0.1.0",
    contact={"email": "angcastillo18@gmail.com", "name": "Angelo Castillo"},
    docs_url=setting.SWAGGER,
    redoc_url=setting.REDOCS,
    exception_handlers=exception_handlers,
    root_path=setting.ROOT_PATH,
)


@app.exception_handler(RequestValidationError)
def request_validation_error(_: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": str(exc), "data": exc.errors()},
    )


# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


load_routes(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
