import jwt

from datetime import datetime, timedelta, UTC
from typing import Optional
from fastapi import Depends, HTTPException, status

from src.secure import oauth2_scheme
from src.configs.app import settings
from src.schemas.auth import AuthUser


def get_new_access_token(
        refresh_token: str,
        refresh_secret: str,
        algorithm: str
) -> str:
    try:
        payload = jwt.decode(refresh_token, refresh_secret,
                             algorithms=[algorithm])
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
            access_token_payload, refresh_secret, algorithm=algorithm)
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


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    refresh_token: Optional[str] = None
):
    """Получение пользователя из JWT-токена."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY_JWT,
                             algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return AuthUser(user_id=user_id)

    except jwt.ExpiredSignatureError:
        if refresh_token:
            new_access_token = get_new_access_token(
                refresh_token,
                settings.REFRESH_SECRET_KEY_JWT,
                settings.ALGORITHM
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token expired, but a new access token has been generated",  # noqa
                headers={"WWW-Authenticate": f"Bearer {new_access_token}"},
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired and no refresh token provided",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
