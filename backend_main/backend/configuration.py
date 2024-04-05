"""Application settings"""

from pydantic_settings import BaseSettings


class Configuration(BaseSettings):
    database_url: str = "postgresql+asyncpg://user:pAssw0rd@10.0.0.15:5432/postgres"
    server_port: int = 8089
    default_timeout: int = 30
    default_workers: int = 1
    log_level: str = "info"


config = Configuration()
