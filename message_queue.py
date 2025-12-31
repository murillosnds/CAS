import os
import json
import pika
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional, Dict, Any

load_dotenv()

class CalculoMessage(BaseModel):
    """Modelo para mensagens de cálculo"""
    peso: float
    idade: int
    atividade: str
    clima: str
    quantidade_de_agua: float
    user_id: Optional[str] = None

class RabbitMQProducer:
    def __init__(self):
        self.host = os.getenv("RABBITMQ_HOST", "rabbitmq")
        self.port = int(os.getenv("RABBITMQ_PORT", 5672))
        self.user = os.getenv("RABBITMQ_USER", "guest")
        self.password = os.getenv("RABBITMQ_PASS", "guest")
        self.queue = os.getenv("RABBITMQ_QUEUE", "ingestao_agua_calculada")
        self.connection = None
        self.channel = None
    
    def connect(self):
        """Estabelece conexão com RabbitMQ"""
        try:
            credentials = pika.PlainCredentials(self.user, self.password)
            parameters = pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                credentials=credentials,
                heartbeat=600,
                blocked_connection_timeout=300
            )
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            # Declara a fila como durável
            self.channel.queue_declare(
                queue=self.queue,
                durable=True
            )
            print("Conectado ao RabbitMQ")
            return True
        except Exception as e:
            print(f"Erro ao conectar ao RabbitMQ: {e}")
            return False
    
    def publish(self, message: Dict[str, Any]):
        """Publica uma mensagem na fila"""
        try:
            if not self.channel or self.connection.is_closed:
                self.connect()
            
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # torna a mensagem persistente
                )
            )
            print(f"Mensagem publicada: {message}")
            return True
        except Exception as e:
            print(f"Erro ao publicar mensagem: {e}")
            return False
    
    def close(self):
        """Fecha a conexão"""
        if self.connection and not self.connection.is_closed:
            self.connection.close()

# Instância global do produtor
rabbitmq_producer = RabbitMQProducer()