from contextlib import asynccontextmanager

import aioredis
from fastapi import FastAPI

from api.v1.endpoints.auth import auth_router
from config.config import settings

from core.db import init_create_tables

from utils.logger import logger

app = FastAPI(
    title=settings.TITLE,
    host=settings.HOST,
    port=settings.PORT,
    version=settings.VERSION,
    debug=settings.DEBUG,

)


# 使用lifespan管理器
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_create_tables()

    logger.info("服务进程启动成功, async")

    yield
    logger.info("服务进程关闭成功, async")


app.lifespan = lifespan

app.include_router(auth_router)
