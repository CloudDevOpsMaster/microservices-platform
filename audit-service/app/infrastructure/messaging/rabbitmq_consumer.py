import json
import asyncio
from typing import Callable
import pika
from pika.adapters.blocking_connection import BlockingConnection
from pika.channel import Channel

from app.infrastructure.config import settings


class RabbitMQConsumer:
    """RabbitMQ consumer for audit events."""
    
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
        
        # Declare exchange
        self.channel.exchange_declare(
            exchange="user.events",
            exchange_type="topic",
            durable=True
        )
        
        # Declare queue
        self.channel.queue_declare(
            queue=self.queue_name,
            durable=True
        )
        
        # Bind queue to exchange with routing patterns
        routing_keys = ["user.*", "auth.*", "audit.*"]
        for routing_key in routing_keys:
            self.channel.queue_bind(
                queue=self.queue_name,
                exchange="user.events",
                routing_key=routing_key
            )
        
        print(f"✅ Connected to RabbitMQ, listening on queue: {self.queue_name}")
    
    def _on_message(self, channel: Channel, method, properties, body: bytes) -> None:
        """Process received message."""
        try:
            message = json.loads(body.decode())
            
            # Run async callback in event loop
            if self._loop and self._loop.is_running():
                asyncio.run_coroutine_threadsafe(
                    self.callback(message),
                    self._loop
                )
            else:
                # Fallback: create new event loop
                asyncio.run(self.callback(message))
            
            # Acknowledge message
            channel.basic_ack(delivery_tag=method.delivery_tag)
            
        except Exception as e:
            print(f"❌ Error processing message: {e}")
            # Reject and requeue message
            channel.basic_nack(
                delivery_tag=method.delivery_tag,
                requeue=True
            )
    
    def start(self, loop=None) -> None:
        """Start consuming messages."""
        self._loop = loop
        self.connect()
        
        # Start consuming
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self._on_message,
            auto_ack=False
        )
        
        print(f"🔄 Started consuming from queue: {self.queue_name}")
        
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self) -> None:
        """Stop consuming messages."""
        self._closing = True
        if self.channel:
            self.channel.stop_consuming()
            self.channel.close()
        if self.connection:
            self.connection.close()
        print("🛑 RabbitMQ consumer stopped")