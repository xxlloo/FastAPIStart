from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.db import get_db_session
from schemas.auth import UserLoginByUserName, UserLoginResponse
from services.auth import AuthService

auth_router = APIRouter()


@auth_router.post("/login/username", response_model=UserLoginResponse)
async def login_phone(
    form_data: UserLoginByUserName, db: AsyncSession = Depends(get_db_session)
):
    return await AuthService.login_username(db, form_data)


@auth_router.post("/refresh_token", response_model=UserLoginResponse)
async def refresh_access_token(
    refresh_token: str, db: AsyncSession = Depends(get_db_session)
):
    return await AuthService.refresh_access_token(db, refresh_token)
