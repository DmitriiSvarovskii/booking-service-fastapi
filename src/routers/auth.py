from fastapi import APIRouter, HTTPException, status

from src.auth.hash_validator import DataValidator
from src.schemas.auth import InitDataRequest
from src.configs.app import settings

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"]
)


@router.post("/validate_data/", status_code=status.HTTP_200_OK)
async def validate_data(request: InitDataRequest):
    try:
        validator = DataValidator(
            bot_token=settings.BOT_TOKEN,
            secret_key_str=settings.SECRET_KEY_STR
        )

        if validator.is_valid_data(request.init_data):
            return {"message": "Data is from Telegram"}
        else:
            raise HTTPException(status_code=400, detail="Data is not valid")

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
