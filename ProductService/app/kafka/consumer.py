import asyncio
from aiokafka import AIOKafkaConsumer
import logging
from google.protobuf.json_format import Parse
from app.proto import product_pb2

logger = logging.getLogger(__name__)

class KafkaConsumer:
    def __init__(self, bootstrap_servers: str, group_id: str, topics: list):
        self.consumer = AIOKafkaConsumer(
            *topics,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            enable_auto_commit=False
        )

    async def start(self):
        await self.consumer.start()

    async def stop(self):
        await self.consumer.stop()

    # async def consume(self):
    #     async for msg in self.consumer:
    #         logger.info(f"Consumed message: {msg.topic}, {msg.partition}, {msg.offset}, {msg.key}, {msg.value}")
    #         try:
    #             product_message = product_pb2.Product()
    #             product_message.ParseFromString(msg.value)
    #             logger.info(f"ProductMessage: {product_message} type {type(product_message)}")
    #             await self.consumer.commit()
    #         except Exception as e:
    #             logger.error(f"Failed to process message: {e}")
    async def consume(self, message_handler):
        async for msg in self.consumer:
            logger.info(f"Consumed message: {msg.topic}, {msg.partition}, {msg.offset}, {msg.key}, {msg.value}")
            try:
                await message_handler(msg)
                await self.consumer.commit()
            except Exception as e:
                logger.error(f"Failed to process message: {e}")

# Singleton instance
kafka_consumer = KafkaConsumer(bootstrap_servers="broker:19092", group_id="my_group", topics=["product_topic"])

# To use the consumer in FastAPI app startup and shutdown events
async def startup_event():
    await kafka_consumer.start()
    asyncio.create_task(kafka_consumer.consume())

async def shutdown_event():
    await kafka_consumer.stop()
