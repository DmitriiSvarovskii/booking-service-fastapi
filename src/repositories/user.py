from typing import List, Optional  # noqa
from fastapi import Depends, HTTPException
from sqlalchemy import insert, select  # noqa
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User
from src.schemas.user import UserCreate
from src.db.postgres import get_async_session


class UserRepository:
    """Класс для работы с таблицей users."""

    @staticmethod
    async def add_user(
        user_data: UserCreate,
        session: AsyncSession = Depends(get_async_session)
    ) -> dict:
        try:
            stmt = insert(User).values(**user_data.model_dump())
            await session.execute(stmt)
            await session.commit()
            return {"status": "success"}
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=400,
                detail="A user with this telegram_id already exists."
            )
        except Exception as e:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Database error: {str(e)}"
            )
