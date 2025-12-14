import json
import pika
from typing import Dict, Any


class RabbitMQPublisher:
    """RabbitMQ message publisher."""
    
    def __init__(self, host: str, port: int, username: str, password: str):
        self.host = host
        self.port = port
        self.credentials = pika.PlainCredentials(username, password)
        self.connection = None
        self.channel = None
    
    def connect(self):
        """Establish connection to RabbitMQ."""
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=self.credentials
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
    
    async def publish(self, routing_key: str, message: Dict[Any, Any]):
        """Publish message to exchange."""
        if not self.channel:
            self.connect()
        
        self.channel.exchange_declare(
            exchange='user_events',
            exchange_type='topic',
            durable=True
        )
        
        self.channel.basic_publish(
            exchange='user_events',
            routing_key=routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # persistent
                content_type='application/json'
            )
        )
    
    def close(self):
        """Close connection."""
        if self.connection:
            self.connection.close()