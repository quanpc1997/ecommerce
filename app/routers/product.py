from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.models.product import ProductSchema
from app.services.product_service import ProductService
from app.repository.product_repository import ProductRepository
from app.entities.product import Product
from uuid import uuid4

router = APIRouter(prefix="/v1/product", tags=["Product"])

async def get_product_service():
    return ProductService(ProductRepository())

@router.post("/create/")
async def create(product: ProductSchema, product_service : ProductService = Depends(get_product_service)):
    product_dict = product.dict()
    new_product = await product_service.create(
        obj=Product(
            _id = str(uuid4()),
            product_name=product_dict["product_name"],
            product_thumb=product_dict["product_thumb"],
            product_description=product_dict["product_description"],
            product_price=product_dict["product_price"],
            product_quantity=product_dict["product_quantity"],
            product_type=product_dict["product_type"],
            product_shop=product_dict["product_shop"],
            product_attributes=product_dict["product_attributes"],
        )
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        "Product": new_product
    })

