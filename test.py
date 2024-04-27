import uuid

import uvicorn
from fastapi import FastAPI, HTTPException
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

# Tạo một instance của FastAPI
app = FastAPI()

# Kết nối tới MongoDB
try:
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["ShopDEV"]
    collection = db["mycollection"]
except Exception as e:
    logger.error("Error: ", e)


# Định nghĩa schema cho dữ liệu đầu vào
class Item(BaseModel):
    name: str
    description: str


# Tạo một API endpoint để thêm một bản ghi mới
@app.post("/items/")
async def create_item(item: Item):
    # Chuyển đổi dữ liệu từ Pydantic model thành dictionary
    item.id = str(uuid.uuid4())
    item_dict = item.dict()
    logger.warning(f"item_dict = {item_dict}")
    # Ghi bản ghi mới vào MongoDB
    result = await collection.insert_one(item_dict)
    logger.warning(f"MMMMMMMMMMMMMMMMm")
    # Trả về thông tin về bản ghi đã được thêm vào
    return {"id": str(result.inserted_id), **item_dict}


@app.post("/do_insert/")
async def do_insert(item: Item):
    document = item.dict()

    result = await db.test_collection.insert_one(document)

    print("result %s" % repr(result.inserted_id))


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=15020)
