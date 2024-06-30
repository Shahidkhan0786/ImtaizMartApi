import asyncio
from aiokafka import AIOKafkaProducer
import logging

logger = logging.getLogger(__name__)

class KafkaProducer:
    def __init__(self, bootstrap_servers: str):
        self.producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send(self, topic: str, key: bytes, value: bytes):
        try:
            await self.producer.send_and_wait(topic, key=key, value=value)
            logger.info(f"Sent message to topic {topic}")
        except Exception as e:
            logger.error(f"Failed to send message to topic {topic}: {e}")

# Singleton instance
kafka_producer = KafkaProducer(bootstrap_servers="broker:19092")

# To use the producer in FastAPI app startup and shutdown events
async def startup_event():
    await kafka_producer.start()

async def shutdown_event():
    await kafka_producer.stop()
