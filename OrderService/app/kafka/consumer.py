import asyncio
from aiokafka import AIOKafkaConsumer
import logging

logger = logging.getLogger(__name__)

class KafkaConsumer:
    def __init__(self, bootstrap_servers: str, group_id: str):
        self.consumer = AIOKafkaConsumer(
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            enable_auto_commit=False
        )
        self.topic_handlers = {}

    async def start(self):
        await self.consumer.start()

    async def stop(self):
        await self.consumer.stop()

    def subscribe(self, topics, handler):
        for topic in topics:
            self.topic_handlers[topic] = handler
        # self.consumer.subscribe(topics)
            current_subscriptions = list(self.topic_handlers.keys())
        self.consumer.subscribe(current_subscriptions)
        logger.info(f"####### Subscription complete. Current handlers: {self.topic_handlers}")

    async def consume(self):
        async for msg in self.consumer:
            logger.info(f"Consumed message: {msg.topic}, {msg.partition}, {msg.offset}, {msg.key}, {msg.value}")
            handler = self.topic_handlers.get(msg.topic)
            if handler:
                try:
                    await handler(msg)
                    await self.consumer.commit()
                except Exception as e:
                    logger.error(f"Failed to process message from topic {msg.topic}: {e}")

# Singleton instance
kafka_consumer = KafkaConsumer(bootstrap_servers="broker:19092", group_id="order_service_group")

# To use the consumer in FastAPI app startup and shutdown events
async def startup_event():
    await kafka_consumer.start()
    asyncio.create_task(kafka_consumer.consume())

async def shutdown_event():
    await kafka_consumer.stop()
