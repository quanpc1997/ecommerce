from app.dbs.mongo import Mongo
from app.entities.api_key import APIKey

from .abstract import BaseRepository


class APIKeyRepository(BaseRepository):
    def __init__(self):
        self.db = Mongo().db["api_key"]

    async def create(self, api_key: APIKey):
        result = await self.db.insert_one(
            {
                "key": api_key.key,
                "status": api_key.status,
                "permissions": api_key.permissions,
            }
        )
        return True

    async def get_by_key(self, key: str):
        await self.db.find_one({"key": key, "status": True})
