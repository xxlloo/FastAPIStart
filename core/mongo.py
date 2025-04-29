from motor.motor_asyncio import AsyncIOMotorClient

from config.config import settings


class MongoDB:
    def __init__(self, uri: str, db_name: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]

    async def close(self):
        self.client.close()


mongodb = MongoDB(
    settings.MONGODB_URL,
    settings.MONGODB_NAME,
)
