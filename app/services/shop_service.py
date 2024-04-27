from .service import Service


class ShopService(Service):
    async def get_by_email(self, email: str):
        return await self._repository.get_by_email(email)
