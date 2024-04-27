from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
import jwt

from app.repository.key_token_repository import KeyTokenRepository
from app.services.key_token_service import KeyTokenService

ALGORITHM_ENCODE = "RS256"

class TokenVerificationMiddleware(BaseHTTPMiddleware):
    
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        #TODO: hoàn thành nốt
        refresh_token = request.headers.get("refresh_token")
        if refresh_token is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request invalid")
        
        key_token = KeyTokenService(KeyTokenRepository).get_by_refresh_token_used(refresh_token)
        if key_token:
            private_key = request.headers.get("private_key")
            if private_key is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request invalid")
            
            # Kiểm tra xem đúng có phải account đó không trong cache xong nếu đúng thì xóa bản ghi đó trong key token. 
    
        # Tìm kiếm token đó có tồn tại hay không bằng cách xem có bản ghi nào có trường refresh_token trùng không.
        # Nếu không thì trả về no chưa đưọc đăng ký


        ## Kiểm tra nếu hết hạn access_token rồi thì cấp mới luôn.


            
        
        
        return await super().dispatch(request, call_next)