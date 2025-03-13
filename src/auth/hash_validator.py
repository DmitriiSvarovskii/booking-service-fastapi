import hmac
import hashlib

from urllib.parse import unquote


class DataValidator:
    def __init__(self, bot_token: str, secret_key_str: str):
        self.bot_token = bot_token
        self.secret_key_str = secret_key_str

    def is_valid_data(self, init_data: str) -> bool:
        """Проверка валидности данных."""

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
            self.secret_key_str.encode(),
            self.bot_token.encode(),
            hashlib.sha256
        ).digest()

        data_check = hmac.new(
            secret_key,
            init_data_to_check.encode(),
            hashlib.sha256
        ).hexdigest()

        return data_check == my_hash
