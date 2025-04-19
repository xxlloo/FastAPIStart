from typing import AsyncGenerator

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.db import session_local


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = session_local()
    try:
        yield async_session
        await async_session.commit()
    except SQLAlchemyError as e:
        await async_session.rollback()
        raise e
    except IntegrityError as e:
        await async_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database integrity error: {str(e)}",
        )
    finally:
        await async_session.close()
