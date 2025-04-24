from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.auth import JwtToken, Users


class AuthCRUD:

    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> Users:
        """
        Get user by username
        :param db:
        :param username:
        :return:
        """
        query = select(Users).where(Users.username == username)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Users:
        """
        Get user by email
        :param db:
        :param email:
        :return:
        """
        query = select(Users).where(Users.email == email)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def insert_jwt_token(db: AsyncSession, jwt_token: JwtToken):
        db.add(jwt_token)
        await db.commit()

    @staticmethod
    async def get_jwt_token(db: AsyncSession, token: str):
        query = select(JwtToken).where(JwtToken.token == token)
        result = await db.execute(query)
        return result.scalars().first()
