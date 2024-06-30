from app.proto import product_pb2, user_pb2
import logging

logger = logging.getLogger(__name__)

user_info_store = {}

async def handle_user_response(msg):
    user_message = user_pb2.User()
    user_message.ParseFromString(msg.value)
    user_info_store[user_message.id] = {
        "id": user_message.id,
        "first_name": user_message.first_name,
        "last_name": user_message.last_name,
        "email": user_message.email
    }
    logger.info(f"Processed user response message: {user_info_store[user_message.id]}")

async def handle_product_event(msg):
    product_message = product_pb2.Product()
    product_message.ParseFromString(msg.value)
    logger.info(f"Processed product event message: {product_message}")
