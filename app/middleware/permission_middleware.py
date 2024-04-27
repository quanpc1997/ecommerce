from fastapi import Request, Depends
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.repository.api_key_repository import APIKeyRepository
from app.services.api_key_service import APIKeyService

from loguru import logger

HEADER = {
    "API_KEY": 'x-api-key',
    "AUTHORIZATION": "authorization"
}


async def get_api_key_service():
    return APIKeyService(APIKeyRepository())


class PermissionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, service: APIKeyService = Depends(get_api_key_service)):
        super().__init__(app)
        self.service = service

    async def dispatch(self, request: Request, call_next):
        try:
            key = request.headers.get(HEADER['API_KEY'])
            if key is None:
                return JSONResponse({
                    "code": 403,
                    "message": "Forbidden Error"
                })
            key_obj = await self.service.get_by_key(key)
            if key_obj is None:
                return JSONResponse({
                    "code": 403,
                    "message": "Forbidden Error"
                })
            request.key_obj = key_obj
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"APIKey is invalid: {e}")
            return e
