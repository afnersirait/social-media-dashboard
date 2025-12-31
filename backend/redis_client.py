import redis
import json
import os
from dotenv import load_dotenv
from typing import Any, Optional

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))


class RedisClient:
    def __init__(self):
        self.client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True
        )

    def get(self, key: str) -> Optional[Any]:
        """Get value from Redis"""
        try:
            value = self.client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Redis GET error: {e}")
            return None

    def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """Set value in Redis with expiration"""
        try:
            self.client.setex(key, expire, json.dumps(value))
            return True
        except Exception as e:
            print(f"Redis SET error: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Delete key from Redis"""
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            print(f"Redis DELETE error: {e}")
            return False

    def exists(self, key: str) -> bool:
        """Check if key exists"""
        try:
            return self.client.exists(key) > 0
        except Exception as e:
            print(f"Redis EXISTS error: {e}")
            return False

    def increment(self, key: str, amount: int = 1) -> int:
        """Increment a counter"""
        try:
            return self.client.incrby(key, amount)
        except Exception as e:
            print(f"Redis INCREMENT error: {e}")
            return 0

    def get_keys(self, pattern: str) -> list:
        """Get all keys matching pattern"""
        try:
            return self.client.keys(pattern)
        except Exception as e:
            print(f"Redis KEYS error: {e}")
            return []


redis_client = RedisClient()
