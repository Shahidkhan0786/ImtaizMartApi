from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Session, select
from app.db.session import get_session
from app.db.models import User, Profile
from app.schemas.user import ProfileCreate, ProfileRead , UserDetail
from app.enums.status_enum import StatusEnum
from app.api.deps import get_current_user

router = APIRouter()


# create profile 
@router.post("/profile", response_model=ProfileRead)
async def create_profile(profile: ProfileCreate, current_user: User = Depends(get_current_user),db: Session = Depends(get_session)):
    # print("In Profle create endpoint")
    db_profile = Profile(
        user_id=current_user.id,
        city=profile.city,
        phone=profile.phone,
        address=profile.address
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


# get login user detail 
@router.get("/detail", response_model=UserDetail)
async def get_user_detail(current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=404, detail="Profile not found")
    return current_user


# get login user profile 
@router.get("/profile", response_model=Profile)
async def get_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    # print("Inn Proile endpoint", current_user)
    result = db.execute(select(Profile).where(Profile.user_id == current_user.id))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
