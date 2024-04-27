from typing import List, Dict, Any

class Product:
    def __init__(
        self,
        _id: str,
        product_name: str,
        product_thumb: str,
        product_description: str,
        product_price: int,
        product_quantity: int,
        product_type: str,
        product_shop: str,
        product_attributes: Any,
    ):
        self._id = _id
        self.product_name = product_name
        self.product_thumb = product_thumb
        self.product_description = product_description
        self.product_price = product_price
        self.product_quantity = product_quantity
        self.product_type = product_type
        self.product_shop = product_shop
        self.product_attributes = product_attributes