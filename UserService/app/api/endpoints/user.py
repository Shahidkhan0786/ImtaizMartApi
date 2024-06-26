from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Session, select
from app.db.session import get_session
from app.db.models import User, Profile
from app.schemas.user import UserCreate, UserRead, ProfileCreate, ProfileRead
from app.enums.status_enum import StatusEnum


router = APIRouter()



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
