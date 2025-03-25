from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    telegram_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    is_premium: bool = False


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
