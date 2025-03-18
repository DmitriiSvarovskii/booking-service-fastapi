import time

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.hash_validator import DataValidator
from src.schemas.auth import InitDataRequest, Token
from src.configs.app import settings

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"]
)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """Получение JWT токенов: access и refresh"""
    if form_data.username == "admin" and form_data.password == "admin":
        validator = DataValidator(
            bot_token=settings.BOT_TOKEN,
            secret_key_str=settings.SECRET_KEY_STR,
            jwt_secret=settings.SECRET_KEY_JWT,
            jwt_refresh_secret=settings.REFRESH_SECRET_KEY_JWT,
            jwt_algorithm=settings.ALGORITHM
        )

        access_token, refresh_token = validator.generate_tokens(
            form_data.username
        )
        print(refresh_token)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
    )


@router.post("/validate_data/", status_code=status.HTTP_200_OK)
async def validate_data(request: InitDataRequest):
    try:
        validator = DataValidator(
            bot_token=settings.BOT_TOKEN,
            secret_key_str=settings.SECRET_KEY_STR,
            jwt_secret=settings.SECRET_KEY_JWT,
            jwt_refresh_secret=settings.REFRESH_SECRET_KEY_JWT,
            jwt_algorithm=settings.ALGORITHM
        )

        if validator.web_app_is_valid_data(request.init_data):
            jwt_token, refresh_token = validator.generate_tokens(1)
            check_jwt = validator.verify_token(jwt_token)
            print("check_jwt: ", check_jwt)
            check_refresh = validator.verify_token(
                refresh_token, is_refresh_token=True)
            print("check_refresh: ", check_refresh)
            time.sleep(3)
            new_check_jwt = validator.verify_token(jwt_token)
            print("new_check_jwt: ", new_check_jwt)
            return {"message": "Data is from Telegram"}
        else:
            raise HTTPException(status_code=400, detail="Data is not valid")

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
