
import logging
import uuid
from app.db.session import get_session
import asyncio
# from app.db.models import User
from app.schemas.token import TokenData
from fastapi import Depends , Header , HTTPException , status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from app.core.config import settings
from app.kafka.producer import kafka_producer
from typing import Annotated , Union
from app.schemas.auth import TokenResponse
from functools import wraps
import json
from app.kafka.handlers import token_response_store

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

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
            logger.warning(f"VALUEEE : {token_response_store}")
            return token_response_store.pop(request_id)
        logger.warning(f"No Object added in token_response_store by handler")
        await asyncio.sleep(settings.RETRY_TIME)  # Wait for second before retrying
    logger.warning(f"No Object added in token_response_store by handler timeout")
    raise HTTPException(status_code=401, detail="Unauthorized")




def role_check(allowed_roles: list[str]):
    
    def check_user_role(current_user: Annotated[Union[TokenResponse, None], Depends(decode_validate_token)]):
        logger.warning(f"CURRENT USER { current_user}")
        if current_user is None or not any(role in current_user.get("roles", []) for role in allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return check_user_role