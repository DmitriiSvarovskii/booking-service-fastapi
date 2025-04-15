from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    MODE: str

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    SERVICE_HOST: str
    SERVICE_PORT: int

    BOT_TOKEN: str
    AUTH_DATE_THRESHOLD: int
    SECRET_KEY_VALIDATE: str

    SECRET_KEY_JWT: str
    REFRESH_SECRET_KEY_JWT: str
    ALGORITHM: str

    ALLOW_METHODS: list[str]
    ALLOW_HOSTS: list[str]
    ALLOW_HEADERS: list[str]
    ALLOW_ORIGINS: list[str]

    SWAGGER_USERNAME: str
    SWAGGER_PASSWORD: str

    RELOAD_FLAG: bool

    LOGS_PATH: str

    @property
    def DB_URL(self):
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8')


settings = Settings()
