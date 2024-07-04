import logging
from app.db.session import get_session
from app.db.models import User
from app.proto import user_pb2
from fastapi import Depends
from app.kafka.producer import kafka_producer
from sqlmodel import Session,select
from app.utils.helper import decode_validate_token
from app.proto import token_validation_pb2
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def handle_validate_token(msg, db: Session):
    print("########## IN VALIDATE TOKEN HANDLER CONSUMER #################################")
    try:
        # token = json.loads(msg.value.decode())
        key = msg.key.decode()       
        token = msg.value.decode()       
        if not token:
            logger.warning("Token is missing in the message")
            validation_result = {"valid": False, "message": "Token is missing"}
            await kafka_producer.send("validate_token_response_topic", key=msg.key ,value=json.dumps(validation_result).encode())
            return
        
        res = decode_validate_token(token , db)
        if not res or res["valid"] == False:
            await kafka_producer.send("validate_token_response_topic",  key=msg.key, value=json.dumps(res).encode())
            return
            
            
        validation_result = {"valid": True, "message": "Token is valid" , "data": res["data"]}
       
        logger.debug(f"Raw message sending in user service: key {msg.key.decode()} value {validation_result}")
        # Create protobuf message
        user_data = token_validation_pb2.UserData(
            user=token_validation_pb2.User(
                id=res["data"]["user"].id,
                first_name=res["data"]["user"].first_name,
                last_name=res["data"]["user"].last_name,
                email=res["data"]["user"].email
            ),
            roles=res["data"]["roles"]
        )

        token_response = token_validation_pb2.ValidateTokenResponse(
            validation_result=token_validation_pb2.ValidationResult(
                valid=validation_result["valid"],
                message=validation_result["message"],
                data=user_data
            )
        )
        # This is a placeholder for actual response logic
        await kafka_producer.send("validate_token_response_topic", key=msg.key, value=token_response.SerializeToString())
        return
    except Exception as e:
        logger.error(f"Error handling token validation: {e}")
        validation_result = {"valid": False, "message": "Internal server error"}
        token_response = token_validation_pb2.ValidateTokenResponse(
            validation_result=token_validation_pb2.ValidationResult(
                valid=validation_result["valid"],
                message=validation_result["message"]
            )
        )
        await kafka_producer.send("validate_token_response_topic", key=msg.key, value=token_response.SerializeToString())

async def handle_user_request(msg, session: Session):
    user_id = int(msg.key.decode())
    logger.info(f"Handling user request message: {msg}")
    
    try:
        user_request = user_pb2.UserRequest()
        user_request.ParseFromString(msg.value)

        user = session.query(User).filter(User.id == user_id).first()
        print(user)


        if user:
            send_user = {
                "id":user.id,
                "email": user.email,
                "first_name":user.first_name,
                "last_name":user.last_name,
            }
            user_response = user_pb2.UserResponse(
                id=user.id,
                user= send_user
            )
            # Send the response back via Kafka or handle it as required
            # logger.info(f"User found: {user_response}")
            # Send the user response message to the response topic
            await kafka_producer.send("user_response_topic", key=str(user_id).encode(), value=user_response.SerializeToString())
            logger.info(f"User response message sent for user ID {user_id}")
          
        else:
            logger.info(f"User not found: {user_id}")
            # Handle user not found case
    except Exception as e:
        logger.error(f"Error handling user request: {e}")
