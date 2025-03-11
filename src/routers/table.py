from typing import Optional, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_async_session


router = APIRouter(
    prefix="/api/v1/table",
    tags=["Table"])


@router.get("/", response_model=List[None])
async def get_all_table(
    session: AsyncSession = Depends(get_async_session)
):
    pass


@router.get("/{id}/", response_model=Optional[None])
async def get_one_table(
    session: AsyncSession = Depends(get_async_session)
):
    pass
