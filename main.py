from fastapi_users import FastAPIUsers
from fastapi import FastAPI

from routers.router_for_auth_users import router as router_for_auth_users
from routers.router_for_all_users import router as router_for_all_users
from auth.auth import auth_backend
from auth.database import User
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate

app = FastAPI(
    title="Referral System"
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

current_user = fastapi_users.current_user()

app.include_router(router_for_auth_users)

app.include_router(router_for_all_users)
