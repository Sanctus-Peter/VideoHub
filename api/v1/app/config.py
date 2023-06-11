from functools import lru_cache
from pathlib import Path
from pydantic import BaseSettings, Field
import os

os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = '1'


class Settings(BaseSettings):
    base_dir: Path = Path(__file__).resolve().parent
    template_dir: Path = base_dir / 'templates'
    keyspace: str = Field(..., env='ASTRADB_KEYSPACE')
    db_client_id: str = Field(..., env='ASTRA_DB_CLIENT_ID')
    db_client_secret: str = Field(..., env='ASTRA_DB_CLIENT_SECRET')
    secret_key: str = Field(..., env='SECRET_KEY')
    algorithm: str = Field(..., env='ALGORITHM')
    access_token_expire_minutes: int = Field(..., env='ACCESS_TOKEN_EXPIRE_MINUTES')
    algolia_index_name: str
    algolia_app_id: str
    algolia_api_key: str

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()
