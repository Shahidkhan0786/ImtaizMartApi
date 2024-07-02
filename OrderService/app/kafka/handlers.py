import logging
from app.db.session import get_session
from app.db.models import User
from app.proto import user_pb2
from fastapi import Depends
from app.kafka.producer import kafka_producer
from sqlmodel import Session,select

logger = logging.getLogger(__name__)

# async def handle_user_request(msg , db:Session):
#     type(msg)
#     print(msg)
#     logger.info(f"Handling user request message: {msg}")
    
#     try:
#         # Parse the incoming message
#         user_request = user_pb2.UserRequest()
#         user_request.ParseFromString(msg.value)
        
#         user_id = user_request.user_id

#         print("User_id is :" , user_id)
#         # user = db.query(User).filter(User.id == user_id).first()
#         result = db.execute(select(User).where(User.id == user_id))
#         user = result.scalar_one_or_none()
#         print("user_request_topic:Consumer fetch user from db")
#         print(user)
#         if not user:
#             logger.error(f"User with ID {user_id} not found.",user)
#             return
        
#         # Prepare the user response message
#         user_response = user_pb2.UserResponse(
#             user_id=user.id,
#             # first_name=user.first_name,
#             # last_name=user.last_name,
#             # email=user.email
#             user=user
#         )
        
#         # Send the user response message to the response topic
#         await kafka_producer.send("user_response_topic", key=str(user_id).encode(), value=user_response.SerializeToString())
#         logger.info(f"User response message sent for user ID {user_id}")
        
#     except Exception as e:
#         logger.error(f"Error handling user request: {e}")

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
