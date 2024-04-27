import uuid

import bcrypt
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.auth.auth_utils import create_token_pair
from app.entities.key_token import KeyToken
from app.entities.shop import Shop
from app.models.shop import ShopSchema
from app.models.key_token import KeyTokenSchema
from app.repository.key_token_repository import KeyTokenRepository
from app.repository.shop_repository import ShopRepository
from app.services.key_token_service import KeyTokenService
from app.services.shop_service import ShopService

from app.helper.rsa import create_rsa_key_pem

from loguru import logger

router = APIRouter(prefix="/v1/shop", tags=["Authen"])


async def get_shop_service():
    return ShopService(ShopRepository())


async def get_key_token_service():
    return KeyTokenService(KeyTokenRepository())


async def hash_password(passwd):
    return bcrypt.hashpw(passwd.encode("utf-8"), bcrypt.gensalt())


@router.post("/signup/")
async def signup(
    shop: ShopSchema,
    shop_service: ShopService = Depends(get_shop_service),
    key_token_service: KeyTokenService = Depends(get_key_token_service),
):
    shop_dict = shop.dict()
    email = await shop_service.get_by_email(shop_dict["email"])
    logger.warning(f"email = {email}")
    if email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This email is existed")

    password_hash = await hash_password(shop_dict["password"])

    shop_id = str(uuid.uuid4())

    new_shop = await shop_service.create(
        obj=Shop(
            shop_id=shop_id,
            name=shop_dict["name"],
            email=shop_dict["email"],
            password=password_hash,
            status=shop_dict["status"],
            verify=shop_dict["verify"],
            roles=shop_dict["roles"],
        )
        )

    public_key_str, private_key_str = await create_rsa_key_pem()

    access_token, refresh_token = await create_token_pair(
        {"user_id": shop_id, "email": shop_dict["email"]},
        public_key_str,
        private_key_str,
    )

    new_key_token = await key_token_service.create(
        obj=KeyToken(
            user_id=shop_id, public_key=public_key_str, refresh_token=refresh_token
        )
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        "metadata": {"user_id": shop_id, "email": shop_dict["email"]},
        "tokens": {
            "access_token": access_token,
            "refresh_token": refresh_token
        },
    })


@router.post("/login/")
async def login(
        email: str, 
        password: str, 
        refresh_token: str = None, 
        shop_service: ShopService = Depends(get_shop_service), 
        key_token_service: KeyTokenService = Depends(get_key_token_service)):
    """
    Quy trình login:
        B1: Check mail in dbs
        B2: Match Password
        B3: Create private key va public key
        B4: generate tokens (Access Token va Refresh Token)
        B5: get data return login
    :param email:
    :param password:
    :param refresh_token:
    :return:
    """
    # B1
    shop_user = shop_service.get_by_email(email)
    if shop_user is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="This user has not registed yet")
    
    # B2
    is_matched = bcrypt.checkpw(password, shop_user.password)

    if not is_matched:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authen error")
    
    # B3:
    public_key_str, private_key_str = await create_rsa_key_pem()

    # B4:
    access_token, refresh_token = await create_token_pair(
        {"user_id": shop_user._id, "email": shop_user.email},
        public_key_str,
        private_key_str,
    )
    
    new_key_token = await key_token_service.create(
        obj=KeyToken(
            user_id=shop_user, public_key=public_key_str, refresh_token=refresh_token
        )
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        "metadata": {"user_id": shop_user._id, "email": shop_user.email},
        "tokens": {
            "access_token": access_token,
            "refresh_token": refresh_token
        },
    })


@router.post("/logout/")
async def logout(key_token: KeyTokenSchema, key_token_service: KeyTokenService = Depends(get_key_token_service)):
    """
    B1: this function related to AuthenticationMiddleware. Please check this
    :param key_token:
    :param key_token_service:
    :return:
    """
    return await key_token_service.remove_by_key_token(key_token._id)