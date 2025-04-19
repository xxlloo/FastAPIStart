from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.config import settings
from core.security import create_access_token, create_refresh_token, verify_token
from curd.auth import AuthCRUD
from models.auth import JwtToken
from schemas.auth import UserLoginByUserName, UserLoginResponse
from utils.password import PasswordUtil


class AuthService:

    @staticmethod
    async def generate_jwt_tokens(user_id: int, username: str) -> list[JwtToken]:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        access_token = create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(
            data={"sub": username}, expires_delta=refresh_token_expires
        )

        return [
            JwtToken(
                user_id=user_id,
                token=access_token,
                expires_at=datetime.now(timezone.utc) + access_token_expires,
                revoked=False,
            ),
            JwtToken(
                user_id=user_id,
                token=refresh_token,
                expires_at=datetime.now(timezone.utc) + refresh_token_expires,
                revoked=False,
            ),
        ]

    @staticmethod
    async def login_username(
        db: AsyncSession,
        form_data: UserLoginByUserName,
    ) -> UserLoginResponse:
        password_util = PasswordUtil()
        selected_user = await AuthCRUD.get_user_by_username(db, form_data.username)

        if not selected_user or not password_util.verify_bcrypt(
            form_data.password, selected_user.password_hash
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        jwt_tokens = await AuthService.generate_jwt_tokens(
            user_id=selected_user.id, username=selected_user.username
        )
        access_token, refresh_token = jwt_tokens

        await AuthCRUD.insert_jwt_token(db, refresh_token)

        return UserLoginResponse(
            access_token=access_token.token,
            refresh_token=refresh_token.token,
            token_type="bearer",
        )

    @staticmethod
    async def refresh_access_token(
        db: AsyncSession, refresh_token: str
    ) -> UserLoginResponse:

        payload = verify_token(refresh_token)

        selected_token = await AuthCRUD.get_jwt_token(db, refresh_token)

        if not payload or not selected_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

        user = await AuthCRUD.get_user_by_username(db, username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )
        return UserLoginResponse(
            access_token=access_token,
            refresh_token=selected_token.token,
            token_type="bearer",
        )
