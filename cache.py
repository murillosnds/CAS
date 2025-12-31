import os
import json
import redis
from dotenv import load_dotenv
from typing import Optional, Any

load_dotenv()

class RedisCache:
    def __init__(self):
        self.host = os.getenv("REDIS_HOST", "redis")
        self.port = int(os.getenv("REDIS_PORT", 6379))
        self.db = int(os.getenv("REDIS_DB", 0))
        self.ttl = int(os.getenv("REDIS_CACHE_TTL", 300))
        self.client = None
        
    def connect(self):
        """Estabelece conexão com Redis"""
        if not self.client:
            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                decode_responses=True,
                socket_connect_timeout=5
            )
        return self.client
    
    def is_connected(self) -> bool:
        """Verifica se o Redis está conectado"""
        try:
            self.connect().ping()
            return True
        except:
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """Obtém valor do cache"""
        try:
            if self.is_connected():
                value = self.client.get(key)
                if value:
                    return json.loads(value)
        except Exception as e:
            print(f"Erro ao obter do Redis: {e}")
        return None
    
    def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Armazena valor no cache"""
        try:
            if self.is_connected():
                ttl = ttl or self.ttl
                self.client.setex(key, ttl, json.dumps(value))
                return True
        except Exception as e:
            print(f"Erro ao salvar no Redis: {e}")
        return False
    
    def delete(self, key: str) -> bool:
        """Remove valor do cache"""
        try:
            if self.is_connected():
                self.client.delete(key)
                return True
        except Exception as e:
            print(f"Erro ao deletar do Redis: {e}")
        return False
    
    def clear_pattern(self, pattern: str) -> int:
        """Remove todas as chaves que correspondem ao padrão"""
        try:
            if self.is_connected():
                keys = self.client.keys(pattern)
                if keys:
                    return self.client.delete(*keys)
        except Exception as e:
            print(f"Erro ao limpar cache: {e}")
        return 0

# Instância global do cache
cache = RedisCache()