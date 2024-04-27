from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.middleware.permission_middleware import PermissionMiddleware
from app.middleware.permission_verification_middleware import PermissionVerificationMiddleware
from app.middleware.authentication_middleware import AuthenticationMiddleware
from app.common.permission import Permission

from app.routers.shop import router as shop_router
from app.routers.api_key import router as api_key_router
from app.routers.product import router as product_router


def create_app():
    app = FastAPI(docs_url="/", redoc_url="/docs")

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    # app.add_middleware(AuthenticationMiddleware)
    # app.add_middleware(PermissionMiddleware)
    # app.add_middleware(PermissionVerificationMiddleware, permission=Permission.READ)

    # Helper
    # count_connection()

    # Routers
    app.include_router(shop_router)
    app.include_router(api_key_router)
    app.include_router(product_router)

    return app
