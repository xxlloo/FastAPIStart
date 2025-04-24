from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.db import get_db_session
from dependencies.email import get_email_sender
from schemas.auth import Register, UserLoginByUserName, UserLoginResponse
from services.auth import AuthService
from utils.email import EmailSender

auth_router = APIRouter()


@auth_router.post("/login/username", response_model=UserLoginResponse)
async def login_phone(
    form_data: UserLoginByUserName,
    db: AsyncSession = Depends(get_db_session, use_cache=True),
):
    return await AuthService.login_username(db, form_data)


@auth_router.post("/refresh_token", response_model=UserLoginResponse)
async def refresh_access_token(
    refresh_token: str, db: AsyncSession = Depends(get_db_session, use_cache=True)
):
    return await AuthService.refresh_access_token(db, refresh_token)


@auth_router.post("/register/send/email")
async def register(
    user: Register,
    bg_task: BackgroundTasks,
    db: AsyncSession = Depends(get_db_session, use_cache=True),
    email_sender: EmailSender = Depends(get_email_sender, use_cache=True),
):
    return await AuthService.send_register_email(db, user, bg_task, email_sender)
