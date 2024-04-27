from typing import TypeVar

from app.repository.shop_repository import ShopRepository

T = TypeVar("T")


class Service:
    def __init__(self, repository):
        self._repository = repository

    async def create(self, obj: T):
        print(f"obj = {obj}")
        return await self._repository.create(obj)
