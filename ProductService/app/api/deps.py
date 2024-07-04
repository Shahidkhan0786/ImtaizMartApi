
import logging
import uuid
from app.db.session import get_session
import asyncio
# from app.db.models import User
# from app.proto import user_pb2
from fastapi import Depends , Header , HTTPException , status
from app.kafka.producer import kafka_producer
from sqlmodel import Session,select
from app.core.config import settings
from app.kafka.producer import kafka_producer
from typing import Annotated , Union
import json
from app.kafka.handlers import token_response_store

logger = logging.getLogger(__name__)

async def decode_validate_token(authorization:Annotated[Union[str, None], Header()] = None , db: Session = Depends(get_session)):
    
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
    
    token = authorization.split(" ")[1] if authorization.startswith("Bearer ") else authorization

    
    if not token:
        logger.warning("Token is missing in the message")
        validation_result = {"valid": False, "reason": "Token is missing"}
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is not valid")
    
    request_id = str(uuid.uuid4())

    await kafka_producer.send("validate_token_topic", key=request_id.encode(),value=str(token).encode())

    # Wait for user info to be available in token_response_store
    for _ in range(settings.RETRY_COUNT):  # Retry  times with a delay
        if request_id in token_response_store:
            return token_response_store.pop(request_id)
        await asyncio.sleep(settings.RETRY_TIME)  # Wait for second before retrying

    raise HTTPException(status_code=401, detail="Unauthorized")



    