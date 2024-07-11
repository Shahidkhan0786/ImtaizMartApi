from jose import JWTError
import jwt
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from datetime import datetime, timezone
from app.schemas.auth import TokenData
from app.db.models import User
from typing import List
from functools import wraps
from app.db.session import get_session
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Configuration
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES




# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         print("#########",payload.get("sub"))
#         username: str = payload.get("sub")
#         roles: list[str] = payload.get("roles", [])
#         if username is None or roles is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Could not validate credentials",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
        
#         user = db.query(User).filter(User.email == username).first()
#         print("user from db", user)
#         if user is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Could not validate credentials",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
#         token_data = TokenData(username=username, roles=roles)
#         return token_data
#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
    
    
def decode_validate_token(token:str , db:Session):
    logger.warning("In decode_validate_token FUNCTION")
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        logger.warning("Token has expired")
        validation_result = {"valid": False, "message": "Token has expired"}
        return validation_result
    except jwt.InvalidTokenError:
        logger.warning("Invalid token")
        validation_result = {"valid": False, "message": "Invalid token"}
        return validation_result

    user_email = payload.get("sub")
    user_roles = payload.get("roles")
    if not user_email:
        logger.warning("Token does not contain user information")
        validation_result = {"valid": False, "message": "Invalid token payload"}
        return validation_result
    
    user = db.query(User).filter(User.email == user_email).first()
    # Check if the token is expired
    expiry = payload.get("exp")
    if expiry and datetime.fromtimestamp(expiry, tz=timezone.utc) < datetime.now(tz=timezone.utc):
        logger.warning("Token has expired")
        validation_result = {"valid": False, "message": "Token has expired"}
        # await kafka_producer.send("validate_token_response_topic", value=json.dumps(validation_result).encode())
        return validation_result
    data = {
        "user":user,
        "roles": user_roles,
        # "exp": expiry,
        # "iat": datetime.fromtimestamp(payload.get("iat"), tz=timezone.utc)
    }
    return {"valid": True , "data": data}

        
    