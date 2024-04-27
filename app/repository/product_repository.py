from .abstract import BaseRepository
from app.dbs.mongo import Mongo
from app.entities.product import Product

class ProductRepository(BaseRepository):
    def __init__(self):
        self.db = Mongo().db["product"]

    async def create(self, product: Product):
        result = await self.db.update_one(
            {"_id": product._id},
            {
                "$set": {
                    "product_name": product.product_name,
                    "product_thumb": product.product_thumb,
                    "product_description": product.product_description,
                    "product_price": product.product_price,
                    "product_quantity": product.product_quantity,
                    "product_type": product.product_type,
                    "product_shop": product.product_shop,
                    "product_attributes": product.product_attributes,
                }
            },
            upsert=True,
        )
        return result
    
    