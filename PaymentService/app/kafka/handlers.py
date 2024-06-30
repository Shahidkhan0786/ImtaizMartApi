import logging
from app.db.session import get_session
from app.db.models import User
from app.proto import user_pb2
from app.kafka.producer import kafka_producer
from sqlmodel import Session

logger = logging.getLogger(__name__)

async def handle_user_request(msg):
    logger.info(f"Handling user request message: {msg}")
    
    try:
        # Parse the incoming message
        user_request = user_pb2.UserRequest()
        user_request.ParseFromString(msg.value)
        
        user_id = user_request.user_id

     
        # db: Session = get_session()
        # user = db.query(User).filter(User.id == user_id).first()
        # Fetch user details from the database
        with get_session() as db:
            user = db.query(User).filter(User.id == user_id).first()
        
        print("user_request_topic:Consumer fetch user from db")
        print(user)
        if not user:
            logger.error(f"User with ID {user_id} not found.")
            return
        
        # Prepare the user response message
        user_response = user_pb2.UserResponse(
            user_id=user.id,
            # first_name=user.first_name,
            # last_name=user.last_name,
            # email=user.email
            user=user
        )
        
        # Send the user response message to the response topic
        await kafka_producer.send("user_response_topic", key=str(user_id).encode(), value=user_response.SerializeToString())
        logger.info(f"User response message sent for user ID {user_id}")
        
    except Exception as e:
        logger.error(f"Error handling user request: {e}")
