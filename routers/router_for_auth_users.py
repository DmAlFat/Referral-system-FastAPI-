from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import auth_backend
from auth.database import User, get_async_session
from auth.manager import get_user_manager
from models.models import user
from string import ascii_letters, digits
from random import sample
from time import time

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

router = APIRouter(
    prefix="/functionality_for_authorized_users",
    tags=["Functionality for authorized users"]
)


@router.get("/create_referral_code")
async def create_referral_code(referral_code_life_time: int, my_user: User = Depends(current_user),
                               session: AsyncSession = Depends(get_async_session)):
    ref_in = ''.join(sample(ascii_letters + digits, 16))
    dt = time() + referral_code_life_time
    stmt = update(user).where(user.c.id == my_user.id).values(referral_code=ref_in, ref_code_death_time=dt)
    await session.execute(stmt)
    await session.commit()
    return f"Your referral code: {ref_in}"


@router.get("/delete_referral_code")
async def delete_referral_code(my_user: User = Depends(current_user),
                               session: AsyncSession = Depends(get_async_session)):
    stmt = update(user).where(user.c.id == my_user.id).values(referral_code='', ref_code_death_time=time())
    await session.execute(stmt)
    await session.commit()
    return f"Your referral code deleted"
