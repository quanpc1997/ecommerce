from typing import List

from pydantic import BaseModel, EmailStr, Field

from app.common.shop_status import ShopStatusEnum


class ShopSchema(BaseModel):
    name: str = Field(max_length=150)
    email: EmailStr = Field(...)
    password: str
    status: ShopStatusEnum
    verify: bool
    roles: List[str]
