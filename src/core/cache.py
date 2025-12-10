import redis
from typing import Optional
from conf import cnf

class CacheClient:
    def __init__(self):
        self.client = redis.Redis(
            host=cnf.redis.host,
            port=cnf.redis.port,
            db=cnf.redis.db,
            password=cnf.redis.pawd,
            decode_responses=True
        )

    def exists(self, key: str) -> bool:
        return self.client.exists(key) == 1

    def set(self, key: str, value: str, ttl: Optional[int] = 3600):
        self.client.set(key, value, ex=ttl)

    def get_str(self, key: str) -> Optional[str]:
        return self.client.get(key)

def get_cache() -> CacheClient:
    return CacheClient()
