from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Session, select
from app.db.session import get_session
from app.db.models import User, Profile
from app.schemas.user import UserCreate, UserRead, ProfileCreate, ProfileRead
from app.enums.status_enum import StatusEnum
from app.api.deps import get_current_user

router = APIRouter()



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

@router.get("/profile/{user_id}", response_model=ProfileRead)
async def read_profile(user_id: int, db: Session = Depends(get_session)):
    result = db.execute(select(Profile).where(Profile.user_id == user_id))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

# get login user profile 
@router.get("/profile", response_model=Profile)
async def get_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    # print("Inn Proile endpoint", current_user)
    # print("Inn Proile endpoint", current_user.id)
    result = db.execute(select(Profile).where(Profile.user_id == current_user.id))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
