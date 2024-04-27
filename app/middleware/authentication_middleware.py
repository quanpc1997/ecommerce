from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException, status, Depends
from app.services.key_token_service import KeyTokenService
from app.repository.key_token_repository import KeyTokenRepository
import jwt

from loguru import  logger


ALGORITHM_ENCODE = "RS256"


class AuthenticationMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        user_id = request.headers.get('"client_id')
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")

        key_token_service = KeyTokenService(KeyTokenRepository())
        key_token = key_token_service.get_by_user_id(user_id)
        if key_token is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid request")

        access_token = request.headers.get("authorization")
        if access_token is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")

        try:
            decode_user = jwt.decode(access_token, key_token.public_key, algorithms=[ALGORITHM_ENCODE])
            if user_id != decode_user.user_id:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid request")
            request.key_token = key_token
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"Can't authentication: {e}")
            return e