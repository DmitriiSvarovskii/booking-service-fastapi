from src.services.data_validator import DataValidator
from src.configs.app import settings


def get_data_validator() -> DataValidator:
    bot_token = settings.BOT_TOKEN
    secret_key_validate = settings.SECRET_KEY_VALIDATE
    return DataValidator(bot_token, secret_key_validate)
