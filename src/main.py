import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import routers
from src.configs.app import settings
from src.docs.main_descriptions import tags_metadata, description


app = FastAPI(
    title="Booking-service-api",
    version="0.0.1a",
    openapi_url="/openapi.json",
    # debug=True
    docs_url="/docs",
    description=description,
    openapi_tags=tags_metadata
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


for router in routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=settings.SERVICE_HOST,
        port=settings.SERVICE_PORT,
        reload=True
    )
