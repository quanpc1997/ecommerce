from .service import Service


class KeyTokenService(Service):
    async def get_by_user_id(self, user_id: str):
        return self._repository.get_by_user_id(user_id)
    
    async def get_by_refresh_token(self, refresh_token: str):
        return self._repository.get_by_refresh_token(refresh_token)

    async def remove_by_key_token(self, _id: str):
        return self._repository.remove_by_key_token(_id)