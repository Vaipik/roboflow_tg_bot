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


class NeuralNetwork(BaseSettings):
    name: str
    version: str


class Settings(BaseSettings):
    bot_token: SecretStr
    db: DataBase
    nn: NeuralNetwork
    roboflow: RoboFlowAPI

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


def load_confg():
    return Settings()
