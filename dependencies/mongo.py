from typing import AsyncGenerator

from core.mongo import MongoDB, mongodb


async def get_mongo_database() -> AsyncGenerator[MongoDB, None]:
    yield mongodb
    await mongodb.close()
