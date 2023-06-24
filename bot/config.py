from pydantic import BaseSettings, SecretStr


class RoboFlow(BaseSettings):
    private_key: str
    publishable_key: str


class Settings(BaseSettings):
    bot_token: SecretStr
    roboflow: RoboFlow

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


cfg = Settings()
