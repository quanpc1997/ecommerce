from typing import List

from app.common.permission import Permission


class APIKey:
    key: str
    status: bool
    permissions: List[Permission] = []
