from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import auth_backend
from auth.database import User, get_async_session
from auth.manager import get_user_manager
from models.models import user

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

router = APIRouter(
    prefix="/functionality for authorized users",
    tags=["Functionality for authorized users"]
)


@router.get("/created_referral_code")
async def created_referral_code(my_user: User = Depends(current_user),
                                session: AsyncSession = Depends(get_async_session)):
    ref_in = 'mortal combat'  # временная реализация
    stmt = update(user).where(user.c.id == my_user.id).values(referral_code=ref_in)
    await session.execute(stmt)
    await session.commit()
    return f"Your referral code: {ref_in}"


@router.get("/deleted_referral_code")
async def deleted_referral_code(my_user: User = Depends(current_user),
                                session: AsyncSession = Depends(get_async_session)):
    stmt = update(user).where(user.c.id == my_user.id).values(referral_code='')
    await session.execute(stmt)
    await session.commit()
    return f"Your referral code deleted"
