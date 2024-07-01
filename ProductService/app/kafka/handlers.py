from app.proto import product_pb2, user_pb2
import logging

logger = logging.getLogger(__name__)

user_info_store = {}

async def handle_user_response(msg):
    print("Handle User response")
    user_message = user_pb2.UserDetailResponse()
    user_message.ParseFromString(msg.value)
    print(user_message)
    user_info_store[user_message.id] = {
        "id": user_message.id,
        "first_name": user_message.user.first_name,
        "last_name": user_message.user.last_name,
        "email": user_message.user.email
    }
    logger.info(f"Processed user response message: {user_info_store[user_message.id]}")

async def handle_product_event(msg):
    product_message = product_pb2.Product()
    product_message.ParseFromString(msg.value)
    logger.info(f"Processed product event message: {product_message}")
