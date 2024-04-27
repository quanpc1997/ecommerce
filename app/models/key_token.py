from pydantic import BaseModel


class KeyTokenSchema(BaseModel):
    user_id: str
    public_key: str
    refresh_token_used: list = []
    refresh_token: str
