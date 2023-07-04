from pydantic import BaseSettings, SecretStr


class DataBase(BaseSettings):
    user: str
    password: str
    host: str
    port: str
    name: str


class RoboFlowAPI(BaseSettings):
    private_key: SecretStr
    publishable_key: SecretStr
    project_id: SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    roboflow: RoboFlowAPI
    db: DataBase

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


cfg = Settings()
