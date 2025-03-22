from src.services.token_generator import TokenGenerator
from src.configs.app import settings


def get_token_generator() -> TokenGenerator:
    jwt_secret = settings.SECRET_KEY_JWT
    refresh_secret = settings.REFRESH_SECRET_KEY_JWT
    jwt_algorithm = settings.ALGORITHM
    return TokenGenerator(jwt_secret, refresh_secret, jwt_algorithm)
