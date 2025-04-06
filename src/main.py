import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import routers
from src.configs.app import settings
from src.docs.main_descriptions import tags_metadata, description
from src.middlewares.check_headers import HeaderValidatorMiddleware


app = FastAPI(
    title="Booking-service-api",
    version="0.0.1a",
    # debug=True
    description=description,
    openapi_tags=tags_metadata
)


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_methods=settings.ALLOW_METHODS,
    allow_headers=settings.ALLOW_HEADERS,
)

for router in routers:
    app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.middleware("http")(HeaderValidatorMiddleware.check_headers)


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=settings.SERVICE_HOST,
        port=settings.SERVICE_PORT,
        reload=True
    )
