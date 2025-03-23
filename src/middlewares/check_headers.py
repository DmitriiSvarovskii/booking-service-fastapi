import logging
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from src.configs.app import settings


class HeaderValidatorMiddleware:
    ALLOWED_PATHS = ["/docs", "/redoc"]

    @classmethod
    async def check_headers(cls, request: Request, call_next):
        if request.url.path in cls.ALLOWED_PATHS:
            return await call_next(request)

        try:
            cls.validate_headers(request)
            return await call_next(request)
        except HTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail},
            )
        except Exception as exc:
            logging.error(f"Unexpected error: {exc}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal Server Error"},
            )

    @staticmethod
    def validate_headers(request: Request):
        host = request.headers.get("host")
        if host not in settings.ALLOW_HOSTS:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden"
            )
