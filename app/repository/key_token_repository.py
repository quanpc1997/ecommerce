from loguru import logger

from app.dbs.mongo import Mongo
from app.entities.key_token import KeyToken
from app.models.key_token import KeyTokenSchema

from .abstract import BaseRepository


class KeyTokenRepository(BaseRepository):
    def __init__(self):
        self.db = Mongo().db["key_token"]

    async def create(self, key_token: KeyToken):
        result = await self.db.update_one(
            {"user_id": key_token.user_id},
            {
                "$set": {
                    "public_key": key_token.public_key,
                    "refresh_token": key_token.refresh_token,
                }
            },
            upsert=True,
        )
        return True

    async def get_by_user_id(self, user_id):
        result = await self.db.find_one(
            {"user_id": user_id}
        )
        return result

    async def remove_by_key_token(self, _id: str):
        result = await self.db.delete_one({"_id": _id})
        return result


    async def get_by_refresh_token_used(self, refresh_token: str):
        result = await self.db.find_one({"refresh_token_used": {"$in": [refresh_token]}})
        return result
    # async def create(self, key_token: KeyToken):
    #     try:
    #         result = await self.db.insert_one(
    #             {
    #                 "user_id": key_token.user_id,
    #                 "public_key": key_token.public_key,
    #                 "refresh_token": key_token.refresh_token
    #             }
    #         )
    #     except Exception as e:
    #         return e
    #     return True
