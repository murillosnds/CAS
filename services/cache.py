import redis
import json
from app.config import get_settings

settings = get_settings()

class CacheService:
    def __init__(self):
        self.redis_client = redis.from_url(settings.redis_url, decode_responses=True)
    
    def get(self, key: str):
        try:
            data = self.redis_client.get(key)
            return json.loads(data) if data else None
        except Exception:
            return None
    
    def set(self, key: str, value: dict, expiration: int = 3600):
        try:
            self.redis_client.setex(key, expiration, json.dumps(value))
        except Exception:
            pass
    
    def generate_key(self, weight: float, age: int, activity: str, climate: str) -> str:
        return f"hydration:{weight}:{age}:{activity}:{climate}"

cache_service = CacheService()