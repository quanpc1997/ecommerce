from typing import List

from pydantic import BaseModel

from app.common.permission import Permission


class APIKey(BaseModel):
    key: str
    status: bool
    permissions: List[Permission]
