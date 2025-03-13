from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    language_code: str
    allows_write_to_pm: bool
    photo_url: str


class TelegramInitData(BaseModel):
    auth_date: int
    query_id: str
    user: str
    hash: str = Field(alias="hash")
