import typing

from app.dbs.mongo import Mongo
from app.entities.shop import Shop

from .abstract import BaseRepository


class ShopRepository(BaseRepository):
    def __init__(self):
        self.db = Mongo().db["shop"]

    async def create(self, shop: Shop):
        result = await self.db.insert_one(
            {
                "_id": shop.shop_id,
                "name": shop.name,
                "email": shop.email,
                "password": shop.password,
                "status": shop.status,
                "verify": shop.verify,
                "roles": shop.roles,
            }
        )
        return True

    async def update(self, shop: Shop):
        result = await self.db.update_one(
            {"id": shop.email},
            {
                "$set": {
                    "name": shop.name,
                    "password": shop.password,
                    "status": shop.status,
                    "verify": shop.verify,
                    "roles": shop.roles,
                }
            },
            upsert=True,
        )
        return result

    async def get_by_email(self, email: str) -> typing.Optional[Shop]:
        return await self.db.find_one({"email": email})
