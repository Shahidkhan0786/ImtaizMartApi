from fastapi import APIRouter, Depends, HTTPException , status
# from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Session, select
from app.db.session import get_session
from app.db.models import User, Profile
from app.schemas.user import UserCreate, UserRead, ProfileCreate, ProfileRead
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.enums.status_enum import StatusEnum
from datetime import timedelta
from app.core.security import create_access_token
from app.schemas.auth import Token , TokenData
from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()

@router.post("/register", response_model=UserRead)
async def register_user(user: UserCreate, db: Session = Depends(get_session)):
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=pwd_context.hash(user.password),
        status=StatusEnum.active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db, email: str, password: str):
    result = db.execute(select(User).where(User.email == email))
    db_user = result.scalar_one_or_none()
    if not db_user or not pwd_context.verify(password, db_user.password):
        return False
    return db_user

@router.post("/login", response_model=TokenData)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    res_data ={
        "first_name": user.first_name,
        "email":user.email,
        "access_token": access_token, 
        "token_type": "bearer"
    }
    return res_data

