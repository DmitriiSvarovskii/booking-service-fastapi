from pydantic import BaseModel


class InitDataRequest(BaseModel):
    init_data: str


class AuthUser(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
