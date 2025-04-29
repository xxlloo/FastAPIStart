import aioredis
from email_validator import validate_email
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.mongo import MongoDB
from dependencies.cache import get_redis
from dependencies.db import get_db_session
from dependencies.email import get_email_sender
from dependencies.mongo import get_mongo_database
from schemas.auth import Register, UserLoginByUserName, UserLoginResponse
from services.auth import AuthService
from tasks.send_email import send_email_task
from utils.email import EmailSender
from utils.logger import logger

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
    redis: aioredis.Redis = Depends(get_redis, use_cache=True),
    mongo: MongoDB = Depends(get_mongo_database, use_cache=True),
):
    logger.info(f"注册用户信息 {user}")
    return await AuthService.send_register_email(
        db, user, bg_task, email_sender, redis, mongo
    )


@auth_router.post("/send-email/")
async def send_email_demo(
    background_tasks: BackgroundTasks,
    email: str = Query(..., description="Recipient email address"),
    subject: str = Query(..., min_length=1),
    body: str = Query(..., min_length=1),
):
    if not validate_email(email):
        raise HTTPException(400, "Invalid email format")
    background_tasks.add_task(send_email_task.apply_async, args=(email, subject, body))
    return {"message": "Email is being sent in the background."}
