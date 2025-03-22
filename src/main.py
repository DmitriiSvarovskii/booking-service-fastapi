import logging
import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.base import BaseHTTPMiddleware

from src.routers import routers
from src.configs.app import settings
# from src.middleware.jwt_middleware import check_jwt_token


app = FastAPI(
    title="Booking-service-api",
    version="0.0.1a",
    openapi_url="/api/v1/openapi.json",
    # debug=True
    docs_url="/api/v1/docs",
    # docs_url=None,
    # redoc_url=None,
)


ORIGINS = [
    "http://localhost",
    "http://localhost:5173",
    "https://api.telegram.org",
]


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=ORIGINS,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type",
                   "Set-Cookie",
                   "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin",
                   "Authorization"],
)

# app.add_middleware(BaseHTTPMiddleware, dispatch=check_jwt_token)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )


for router in routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=settings.SERVICE_HOST,
        port=settings.SERVICE_PORT,
        reload=True
    )
