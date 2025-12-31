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
```

### 11. app/tasks/worker.py
```python
import pika
import json
import time
from app.config import get_settings

settings = get_settings()

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"[Worker] Processando cálculo: {data}")
    
    # Simulação de processamento assíncrono
    time.sleep(2)
    
    print(f"[Worker] Cálculo processado com sucesso!")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_worker():
    connection = pika.BlockingConnection(pika.URLParameters(settings.rabbitmq_url))
    channel = connection.channel()
    
    channel.queue_declare(queue='hydration_calculations', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='hydration_calculations', on_message_callback=callback)
    
    print('[Worker] Aguardando mensagens...')
    channel.start_consuming()

if __name__ == '__main__':
    start_worker()