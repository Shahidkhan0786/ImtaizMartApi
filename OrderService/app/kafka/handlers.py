from app.proto import user_pb2
from app.proto import token_validation_pb2
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

user_info_store = {}
token_response_store = {}

# validate token response consumer 
async def handle_validate_token_responses(msg):
    try:
        logger.info("Handling validate token response...")
        
         # Log the raw message content
        logger.debug(f"Raw message received: key {msg.key.decode()} value {msg.value}")
        print(f"Raw message received: {msg.value}")
        
        # Parse the message
        user_message = token_validation_pb2.ValidateTokenResponse()
        user_message.ParseFromString(msg.value)
        
        # Access parsed data
        validation_result = user_message.validation_result
        if validation_result.valid:
            user_data = validation_result.data
            user_info = user_data.user
            user_role = user_data.roles
            logger.info(f"Key is {msg.key.decode()}")
            logger.info(f"Valid token for user: id: {user_info.id} , {user_info.first_name} {user_info.last_name} ({user_info.email}) and role is {user_role}")
            token_response_store[msg.key.decode()] = {
                "id": user_info.id,
                "first_name": user_info.first_name,
                "last_name": user_info.last_name,
                "email": user_info.email,
                "roles": user_role,
                "token_valid": validation_result.valid,
                "token_message": validation_result.message,
            }
            return
        else:
            logger.warning(f"Token validation failed: {validation_result.message}")
            return False
    
    except Exception as e:
        logger.error(f"Failed to process message from topic {msg.topic}: {e}")
        return False

    

    
async def handle_user_response(msg):
    try:
        logger.info("Handle User response")
        user_message = user_pb2.UserDetailResponse()
        user_message.ParseFromString(msg.value)
        logger.debug(f"Parsed user message: {user_message}")
        
        user_info_store[user_message.id] = {
            "id": user_message.id,
            "first_name": user_message.user.first_name,
            "last_name": user_message.user.last_name,
            "email": user_message.user.email
        }
        
        logger.info(f"Processed user response message: {user_info_store[user_message.id]}")
    
    except Exception as e:
        logger.error(f"Error processing user response message: {e}")
        logger.debug(f"Failed message details: {msg}")


# async def handle_product_event(msg):
#     product_message = product_pb2.Product()
#     product_message.ParseFromString(msg.value)
#     logger.info(f"Processed product event message: {product_message}")
