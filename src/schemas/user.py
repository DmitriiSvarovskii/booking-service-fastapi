import datetime

from typing import Optional
from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    telegram_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    birth_day: Optional[datetime.datetime] = None
    is_premium: bool
    is_active: bool
