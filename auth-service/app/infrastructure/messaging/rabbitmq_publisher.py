import pika
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class RabbitMQPublisher:
    """RabbitMQ message publisher."""
    
    def __init__(self, host: str, port: int, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None
        self.channel = None
    
    def connect(self) -> None:
        """Initialize RabbitMQ connection."""
        try:
            credentials = pika.PlainCredentials(self.username, self.password)
            parameters = pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                credentials=credentials,
                heartbeat=600,
                blocked_connection_timeout=300
            )
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            
            # Declare exchange
            self.channel.exchange_declare(
                exchange='auth.events',
                exchange_type='topic',
                durable=True
            )
            logger.info("RabbitMQ connection established")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise
    
    def disconnect(self) -> None:
        """Close RabbitMQ connection."""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            logger.info("RabbitMQ connection closed")
    
    async def publish(self, routing_key: str, message: Dict[Any, Any]) -> None:
        """
        Publish message to exchange.
        
        Args:
            routing_key: Routing key for the message
            message: Message payload as dictionary
        """
        try:
            if not self.channel or self.connection.is_closed:
                self.connect()
            
            self.channel.basic_publish(
                exchange='auth.events',
                routing_key=routing_key,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                    content_type='application/json'
                )
            )
            logger.info(f"Published message to {routing_key}")
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            # Attempt reconnection
            self.connect()
            raise