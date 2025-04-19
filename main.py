from contextlib import asynccontextmanager

from fastapi import FastAPI

from config.config import settings
from core.db import init_create_tables
from utils.logger import logger


# 使用lifespan管理器
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_create_tables()
    logger.info("服务进程启动成功, async")

    yield
    logger.info("服务进程关闭成功, async")


app = FastAPI(
    debug=settings.debug,
    title=settings.title,
    description=settings.description,
    version=settings.version,

    lifespan=lifespan,
)


@app.get("/")
async def read_root():
    logger.info("fastapi running")

    return {
        "database_url": settings.ASYNC_DATABASE_URI,
    }
