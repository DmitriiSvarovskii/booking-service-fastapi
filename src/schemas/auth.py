from typing import Optional
from pydantic import BaseModel


class InitDataRequest(BaseModel):
    init_data: str


class AuthUser(BaseModel):
    user_id: int

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenResponse(Token):
    pass
