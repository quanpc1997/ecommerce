import motor.motor_asyncio
from loguru import logger


class Mongo:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = None
            cls._instance.db = None
            # Thiết lập kết nối tại đây
            try:
                cls._instance.client = motor.motor_asyncio.AsyncIOMotorClient(
                    "mongodb://localhost:27017/"
                )
                cls._instance.db = cls._instance.client["ShopDEV"]
            except Exception as e:
                logger.error(e)
                return e
        return cls._instance
