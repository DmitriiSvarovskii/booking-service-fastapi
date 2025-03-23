from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.schemas.auth import InitDataRequest, TokenResponse
from src.services.token_generator import TokenGenerator
from src.services.data_validator import DataValidator
from src.dependencies.token_generator import get_token_generator
from src.dependencies.data_validator import get_data_validator
from src.docs import auth_descriptions
from src.configs.app import settings


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post(
    "/validate_data/",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary=auth_descriptions.VALIDATE_DATA_SUMMARY,
    description=auth_descriptions.VALIDATE_DATA_DESCRIPTION
)
async def validate_data(
    request: InitDataRequest,
    validator: DataValidator = Depends(get_data_validator),
    token_generator: TokenGenerator = Depends(get_token_generator)
):
    try:
        if validator.web_app_is_valid_data(request.init_data):
            user_id = validator.get_user_id(request.init_data)
            jwt_token, refresh_token = token_generator.generate_tokens(
                user_id)

            return TokenResponse(
                access_token=jwt_token,
                refresh_token=refresh_token
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data is not valid"
            )

    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


@router.post(
    "/token",
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse,
    include_in_schema=False
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    token_generator: TokenGenerator = Depends(get_token_generator)

):
    """Получение JWT токенов: access и refresh"""
    if (
        form_data.username == settings.SWAGGER_USERNAME
    ) and (
        form_data.password == settings.SWAGGER_PASSWORD
    ):
        jwt_token, refresh_token = token_generator.generate_tokens(1)

        return TokenResponse(
            access_token=jwt_token,
            refresh_token=refresh_token
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
    )
