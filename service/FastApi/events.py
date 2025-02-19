import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI

from internal.api import routers
from config.config import config
from internal.entities.database.base import create_async_database, close_database

logger = logging.getLogger(__name__)


async def create_start_app_handler():
    """Инициализация базы данных."""
    logger.info("Инициализация базы данных...")
    await create_async_database()
    logging.info("База данных успешно инициализирована.")


async def shutdown_app_handler():
    logging.info("Закрытие соединений с базой данных...")
    await close_database()
    logging.info("Соединения успешно закрыты.")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    logging.info("FastAPI стартует...")
    # await create_start_app_handler()
    yield
    # await shutdown_app_handler()
    logging.info("FastAPI завершает работу...")


def create_fastapi() -> FastAPI:
    application = FastAPI(
        lifespan=lifespan,
        title="API",
        description="Получение данных магазинов",
    )
    application.include_router(routers)
    return application


async def start_fastapi(app=FastAPI):
    # Запускаем Uvicorn сервер

    cfg = uvicorn.Config(app,
                            host=config.server.host.replace("https://", ""),
                            port=config.server.port,
                            ssl_keyfile="data/server.key",
                            ssl_certfile="data/server.crt"
                            )
    server = uvicorn.Server(cfg)
    await server.serve()
