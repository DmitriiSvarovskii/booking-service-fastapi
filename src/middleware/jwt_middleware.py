import jwt
from fastapi import HTTPException, Request
from typing import Callable
from src.configs.app import settings


SECRET_KEY = settings.SECRET_KEY_JWT
ALGORITHM = "HS256"


async def check_jwt_token(request: Request, call_next: Callable):
    if request.url.path.startswith('/api/v1/docs') or request.url.path == '/api/v1/openapi.json' or request.url.path == '/api/v1/auth/token':  # noqa
        return await call_next(request)

    token = request.headers.get("Authorization")

    if token is None:
        raise HTTPException(
            status_code=401, detail="Authorization token missing")

    if not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = token.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if "sub" not in payload:
            raise HTTPException(status_code=401, detail="Invalid token")

        request.state.user_id = payload["sub"]

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    response = await call_next(request)
    return response
