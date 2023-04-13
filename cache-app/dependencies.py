from functools import lru_cache
from typing import Optional

from config import Settings
from db import Redis


@lru_cache()
def get_redis_conn() -> Optional[Redis.connect]:
    return Redis.connect()


@lru_cache()
def get_settings() -> Optional[Settings]:
    return Settings()
