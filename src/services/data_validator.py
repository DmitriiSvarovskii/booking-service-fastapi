import hmac
import hashlib
import json

from urllib.parse import unquote


class DataValidator:
    def __init__(
        self,
        bot_token: str,
        secret_key_validate: str,
    ):
        self.bot_token = bot_token
        self.secret_key_validate = secret_key_validate

    def web_app_is_valid_data(self, init_data: str) -> bool:
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
            self.secret_key_validate.encode(),
            self.bot_token.encode(),
            hashlib.sha256
        ).digest()

        data_check = hmac.new(
            secret_key,
            init_data_to_check.encode(),
            hashlib.sha256
        ).hexdigest()

        return data_check == my_hash

    def get_user_id(self, init_data: str) -> int:
        init_data = unquote(init_data)
        params = dict(chunk.split("=") for chunk in init_data.split("&"))

        user_data_str = params.get("user")

        if user_data_str:
            try:
                user_data = json.loads(user_data_str)
                return int(user_data.get("id", 0))
            except json.JSONDecodeError:
                raise ValueError("Failed to decode 'user' parameter as JSON")
        else:
            raise ValueError("'user' parameter is missing or invalid")
