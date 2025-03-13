import hmac
import hashlib

from urllib.parse import unquote

from src.configs.app import settings


def is_valid_data(init_data: str) -> bool:
    init_data = unquote(init_data)

    params = dict(chunk.split("=") for chunk in init_data.split("&"))

    my_hash = params.get("hash")

    if not my_hash:
        print("Hash not found!")
        return False

    params.pop("hash", None)

    init_data_to_check = "\n".join(
        [f"{key}={value}" for key, value in sorted(params.items())])

    secret_key = hmac.new(
        settings.SECRET_KEY_STR.encode(),
        settings.BOT_TOKEN.encode(),
        hashlib.sha256
    ).digest()

    data_check = hmac.new(
        secret_key,
        init_data_to_check.encode(),
        hashlib.sha256
    ).hexdigest()

    return data_check == my_hash
