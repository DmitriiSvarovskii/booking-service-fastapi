import jwt

from datetime import datetime, timedelta, UTC
from fastapi import status, HTTPException


class TokenGenerator:
    def __init__(
        self,
        jwt_secret: str,
        refresh_secret: str,
        jwt_algorithm: str
    ):
        self.jwt_secret = jwt_secret
        self.refresh_secret = refresh_secret
        self.jwt_algorithm = jwt_algorithm

    def generate_token(self, user_id: int, exp_delta: timedelta) -> str:
        payload = {
            "sub": str(user_id),
            "exp": datetime.now(UTC) + exp_delta,
            "iat": datetime.now(UTC)
        }

        return jwt.encode(
            payload,
            self.jwt_secret,
            algorithm=self.jwt_algorithm
        )

    def generate_tokens(self, user_id: int) -> tuple:
        """
        Генерирует два токена: access_token и refresh_token
        """
        access_exp_delta = timedelta(minutes=15)
        access_token = self.generate_token(user_id, access_exp_delta)

        refresh_exp_delta = timedelta(days=30)
        refresh_token = self.generate_token(user_id, refresh_exp_delta)

        return access_token, refresh_token

    def decode_token(self, token: str) -> dict:
        return jwt.decode(
            token,
            self.jwt_secret,
            algorithms=[self.jwt_algorithm]
        )

    def get_new_access_token(
        self,
        refresh_token: str,
        refresh_secret: str,
    ) -> str:
        try:
            payload = jwt.decode(refresh_token, self.refresh_secret,
                                 algorithms=[self.jwt_algorithm])
            user_id = payload.get("sub")

            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token",
                )

            access_token_payload = {
                "sub": user_id,
                "exp": datetime.now(UTC) + timedelta(minutes=30),
                "iat": datetime.now(UTC)
            }
            new_access_token = jwt.encode(
                access_token_payload,
                refresh_secret,
                algorithm=self.jwt_algorithm
            )
            return new_access_token

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired",
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )
