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