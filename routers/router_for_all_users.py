from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from auth.database import get_async_session
from models.models import user

router = APIRouter(
    prefix="/functionality for all users",
    tags=["Functionality for all users"]
)


@router.get("/")
async def get_referral_code(email: str, session: AsyncSession = Depends(get_async_session)):
    query = select(user.c.referral_code).select_from(user).where(user.c.email == email)
    result = await session.execute(query)
    res_out = result.one()
    return f"{res_out[0]}"


@router.post("/")
async def receive_info_on_referrals(user_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(user.c.referrals).select_from(user).where(user.c.id == user_id)
    result = await session.execute(query)
    try:
        res_out = result.one()
        return f"{res_out[0]}"
    except:
        return f"User with this id is not registered"
