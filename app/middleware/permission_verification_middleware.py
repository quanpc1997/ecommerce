from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import Request

from loguru import logger


class PermissionVerificationMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, permission: str):
        super().__init__(app)
        self.permission = permission

    async def dispatch(self, request: Request, call_next):
        try:
            if request.key_obj.permissions: # if empty
                return JSONResponse({
                    "code": 403,
                    "message": "Permission denied"
                })

            logger.debug(f"Permission: {request.key_obj.permissions}")
            if self.permission not in request.key_obj.permissions:
                return JSONResponse({
                    "code": 403,
                    "message": "Permission denied"
                })
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"Can't check the permission is valid or not: {e}")

