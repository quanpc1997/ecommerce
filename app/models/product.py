from pydantic import BaseModel, Field
from fastapi import Path
from app.common.product_type import ProductType
from typing import Any

class ProductSchema(BaseModel):
    product_name: str
    product_thumb: str
    product_slug: str #VD: quan-jean-cao-cap
    product_description: str
    product_price: int = Path(..., ge=0)
    product_quantity: int = Path(..., ge=0)
    product_type: ProductType
    product_shop: str
    product_attributes: Any
