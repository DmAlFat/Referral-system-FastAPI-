from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models, schemas
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from auth.database import User, get_user_db, get_async_session
from models.models import user

SECRET = "MYSTERY"


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")

        ref_code = str(user_dict.pop("referral_code"))
        mail = user_dict['email']

        async def add_referrals(ref_code_in: ref_code, session: AsyncSession = get_async_session()):
            stmt = update(user).where(user.c.referral_code == ref_code_in).values(referrals=mail)
            await session.execute(stmt)
            await session.commit()
            return {"status": "success"}

        if ref_code is not None:
            await add_referrals(ref_code)

        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["referral_code"] = ""
        user_dict["referrals"] = {}

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
