import os
import json
import pika
from dotenv import load_dotenv

load_dotenv()

class RabbitMQConsumer:
    def __init__(self):
        self.host = os.getenv("RABBITMQ_HOST", "rabbitmq")
        self.port = int(os.getenv("RABBITMQ_PORT", 5672))
        self.user = os.getenv("RABBITMQ_USER", "guest")
        self.password = os.getenv("RABBITMQ_PASS", "guest")
        self.queue = os.getenv("RABBITMQ_QUEUE", "ingestao_agua_calculada")
    
    def callback(self, ch, method, properties, body):
        """Processa mensagens recebidas"""
        try:
            message = json.loads(body)
            print(f"📥 Mensagem recebida: {message}")
            
            # Aqui você pode adicionar lógica de processamento
            # Ex: enviar email, notificação, analytics, etc.
            
            # Confirma o processamento
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        except Exception as e:
            print(f"❌ Erro ao processar mensagem: {e}")
    
    def start_consuming(self):
        """Inicia o consumo de mensagens"""
        try:
            credentials = pika.PlainCredentials(self.user, self.password)
            parameters = pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                credentials=credentials
            )
            
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            
            # Garante que a fila existe
            channel.queue_declare(queue=self.queue, durable=True)
            
            # Configura QoS
            channel.basic_qos(prefetch_count=1)
            
            # Inicia consumo
            channel.basic_consume(
                queue=self.queue,
                on_message_callback=self.callback
            )
            
            print("🚀 Consumer iniciado. Aguardando mensagens...")
            channel.start_consuming()
            
        except KeyboardInterrupt:
            print("👋 Consumer finalizado pelo usuário")
        except Exception as e:
            print(f"❌ Erro no consumer: {e}")

if __name__ == "__main__":
    consumer = RabbitMQConsumer()
    consumer.start_consuming()