import json
import asyncio
from typing import Callable
import pika
from pika.adapters.blocking_connection import BlockingConnection
from pika.channel import Channel
import logging
from app.core.config import get_settings

settings = get_settings()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RabbitMQConsumer:
    """RabbitMQ consumer for user events."""
    
    def __init__(self, queue_name: str, callback: Callable):
        self.queue_name = queue_name
        self.callback = callback
        self.connection: BlockingConnection | None = None
        self.channel: Channel | None = None
        self._closing = False
        self._loop = None
    
    def connect(self) -> None:
        """Establish RabbitMQ connection."""
        parameters = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            credentials=pika.PlainCredentials(
                settings.RABBITMQ_USER,
                settings.RABBITMQ_PASSWORD
            ),
            heartbeat=600,
            blocked_connection_timeout=300
        )
        
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        
        # Declare exchange (mismo que auth-service)
        self.channel.exchange_declare(
            exchange='user.events',
            exchange_type='topic',
            durable=True
        )
        
        # Declare queue
        self.channel.queue_declare(
            queue=self.queue_name,
            durable=True
        )
        
        # Bind queue to exchange with routing key
        self.channel.queue_bind(
            exchange='user.events',
            queue=self.queue_name,
            routing_key='user.created'
        )
        
        logger.info(f"✅ User Service: Connected to RabbitMQ")
        logger.info(f"   - Exchange: user.events")
        logger.info(f"   - Queue: {self.queue_name}")
        logger.info(f"   - Routing Key: user.created")
    
    def _on_message(self, channel: Channel, method, properties, body: bytes) -> None:
        """Process received message."""
        try:
            message = json.loads(body.decode())
            logger.info(f"📥 User Service received: {message.get('event_type')}")
            
            # Run async callback
            if self._loop and self._loop.is_running():
                asyncio.run_coroutine_threadsafe(
                    self.callback(message),
                    self._loop
                )
            else:
                asyncio.run(self.callback(message))
            
            # Acknowledge message
            channel.basic_ack(delivery_tag=method.delivery_tag)
            logger.info(f"✅ User Service: Message processed")
            
        except Exception as e:
            logger.error(f"❌ User Service error: {e}")
            import traceback
            traceback.print_exc()
            # Reject and requeue
            channel.basic_nack(
                delivery_tag=method.delivery_tag,
                requeue=True
            )
    
    def start(self, loop=None) -> None:
        """Start consuming messages."""
        self._loop = loop
        self.connect()
        
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self._on_message,
            auto_ack=False
        )
        
        logger.info(f"🔄 User Service: Started consuming messages")
        
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self) -> None:
        """Stop consuming."""
        self._closing = True
        if self.channel and self.channel.is_open:
            self.channel.stop_consuming()
            self.channel.close()
        if self.connection and self.connection.is_open:
            self.connection.close()
        logger.info("🛑 User Service consumer stopped")