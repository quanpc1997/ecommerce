from typing import List
import uuid

class KeyToken:
    def __init__(self, user_id: str, public_key: str, refresh_token: str):
        self._id = str(uuid.uuid4())
        self.user_id = user_id
        self.public_key = public_key
        self.refresh_token: str = refresh_token
        self.refresh_token_used: List[str] = []
        
