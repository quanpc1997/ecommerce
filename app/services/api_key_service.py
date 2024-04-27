from .service import Service


class APIKeyService(Service):
    async def get_by_key(self, key: str):
        return await self._repository.get_by_email(key)
