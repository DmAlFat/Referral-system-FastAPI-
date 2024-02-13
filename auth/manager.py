from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models, schemas
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.database import User, get_user_db, engine
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
        res = []

        if ref_code != "":
            async with AsyncSession(autoflush=False, bind=engine) as sess:
                query = select(user).where(user.c.referral_code == ref_code)
                result = await sess.execute(query)
                res = result.all()
        if len(res) > 0:
            ref_in = res[0][5]
            ref_in[user_dict['email']] = user_dict['username']
            async with AsyncSession(autoflush=False, bind=engine) as session:
                stmt = update(user).where(user.c.referral_code == ref_code).values(referrals=ref_in)
                await session.execute(stmt)
                await session.commit()

        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["referral_code"] = ""
        user_dict["referrals"] = {}

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
