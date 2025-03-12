import json
import time
import hashlib
import hmac

from urllib.parse import unquote
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ValidationError

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth (test)"]
)

BOT_TOKEN = '6141111072:AAH8CBhf7iQUVNFCjR_STaBf9h_mYHSggvo'
# c_str = "WebAppData"
C_STR = "WebAppData"
AUTH_DATE_THRESHOLD = 86400


class TelegramUser(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    language_code: str
    is_premium: bool
    allows_write_to_pm: bool


class TelegramAuthData(BaseModel):
    query_id: str
    user: str
    auth_date: int


def is_valid_data(data_check_string: str) -> bool:
    init_data = unquote(unquote(data_check_string))
    data_dict = dict(chunk.split("=", 1) for chunk in init_data.split("&"))

    data_hash = data_dict.pop("hash", None)
    if not data_hash:
        print("Hash not found in data!")
        return False

    try:
        auth_data = TelegramAuthData(**data_dict)
        auth_data.user = TelegramUser(
            **json.loads(auth_data.user))
    except ValidationError as e:
        print(f"Validation error: {e}")
        return False

    if time.time() - auth_data.auth_date > AUTH_DATE_THRESHOLD:
        print("Auth date is too old!")
        return False

    data_sorted = sorted(data_dict.items(), key=lambda x: x[0])
    data_string = "\n".join([f"{key}={value}" for key, value in data_sorted])

    secret_key = hmac.new(
        C_STR.encode(), BOT_TOKEN.encode(), hashlib.sha256).digest()

    calculated_hash = hmac.new(
        secret_key, data_string.encode(), hashlib.sha256).hexdigest()

    return calculated_hash == data_hash


@router.post("/validate_data/", status_code=status.HTTP_200_OK)
async def validate_data(data_check_string: str) -> dict:
    if is_valid_data(data_check_string):
        return {"message": "Data is from Telegram"}
    else:
        raise HTTPException(status_code=400, detail="Data is not valid")
