from typing import Optional, List  # noqa
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.user import UserRepository
from src.schemas.user import UserCreate
from src.db.postgres import get_async_session


router = APIRouter(
    prefix="/api/v1/user",
    tags=["User"])


@router.post(
    "/",
    response_model=dict,
    status_code=status.HTTP_201_CREATED
)
async def get_all_table(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_async_session)
):
    new_user = await UserRepository.add_user(
        user_data=user_data,
        session=session
    )
    return new_user
