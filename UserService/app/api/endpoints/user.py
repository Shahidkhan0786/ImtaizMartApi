from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Session, select
from app.db.session import get_session
from app.db.models import User, Profile
from app.schemas.user import UserCreate, UserRead, ProfileCreate, ProfileRead
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()

@router.post("/register", response_model=UserRead)
async def register_user(user: UserCreate, db: Session = Depends(get_session)):
    db_user = User(
        firstName=user.firstName,
        lastName=user.lastName,
        email=user.email,
        password=pwd_context.hash(user.password),
        status=StatusEnum.active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
async def login_user(email: str, password: str, db: Session = Depends(get_session)):
    result = db.execute(select(User).where(User.email == email))
    db_user = result.scalar_one_or_none()
    if not db_user or not pwd_context.verify(password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful"}

@router.post("/profile", response_model=ProfileRead)
async def create_profile(profile: ProfileCreate, db: Session = Depends(get_session)):
    db_profile = Profile(
        user_id=profile.user_id,
        city=profile.city,
        phone=profile.phone,
        address=profile.address
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.get("/profile/{user_id}", response_model=ProfileRead)
async def read_profile(user_id: int, db: Session = Depends(get_session)):
    result = db.execute(select(Profile).where(Profile.user_id == user_id))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
