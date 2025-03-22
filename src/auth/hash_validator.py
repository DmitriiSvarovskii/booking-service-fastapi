import hmac
import hashlib

from urllib.parse import unquote
from fastapi import HTTPException, status
import jwt
from datetime import datetime, timedelta, UTC
# from typing import Tuple


class DataValidator:
    def __init__(
        self,
        bot_token: str,
        secret_key_str: str,
        jwt_secret: str,
        jwt_refresh_secret: str,
        jwt_algorithm: str = "HS256"
    ):
        self.bot_token = bot_token
        self.secret_key_str = secret_key_str
        self.jwt_secret = jwt_secret
        self.jwt_refresh_secret = jwt_refresh_secret
        self.jwt_algorithm = jwt_algorithm

    def generate_tokens(self, user_id: int) -> tuple[str, str]:
        """Генерация JWT access token и refresh token."""

        def create_token(secret: str, exp_delta: timedelta) -> str:
            payload = {
                "sub": str(user_id),
                "exp": datetime.now(UTC) + exp_delta,
                "iat": datetime.now(UTC)
            }
            return jwt.encode(payload, secret, algorithm=self.jwt_algorithm)

        return create_token(self.jwt_secret, timedelta(minutes=1)), \
            create_token(self.jwt_refresh_secret, timedelta(days=7))

    def verify_token(self, token: str, is_refresh_token: bool = False) -> dict:
        """Декодирование и проверка JWT токена."""
        try:
            secret_key = (
                self.jwt_refresh_secret
                if is_refresh_token
                else self.jwt_secret
            )

            payload = jwt.decode(token, secret_key, algorithms=[
                self.jwt_algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired. Please refresh your token."
            )
        except jwt.InvalidTokenError as e:
            print(f"Invalid token error: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

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

    def get_user_id(self, init_data: str) -> int:
        init_data = unquote(init_data)
        params = dict(chunk.split("=") for chunk in init_data.split("&"))
        return int(params.get("user"))
