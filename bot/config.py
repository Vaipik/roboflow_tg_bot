from pydantic import BaseSettings, SecretStr


class RoboFlowAPI(BaseSettings):
    private_key: SecretStr
    publishable_key: SecretStr
    project_id: SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    roboflow: RoboFlowAPI

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


cfg = Settings()
