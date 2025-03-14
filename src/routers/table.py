from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_async_session
from src.schemas.table import TableGet
from src.repositories.table import TableRepository


router = APIRouter(
    prefix="/api/v1/table",
    tags=["Table"])


@router.get("/", response_model=List[TableGet])
async def get_all_table(
    session: AsyncSession = Depends(get_async_session)
):
    tables = await TableRepository.get_all_table(
        session=session
    )
    return tables


@router.get("/{id}/", response_model=TableGet)
async def get_one_table(
    id: int,
    session: AsyncSession = Depends(get_async_session)
):
    table = await TableRepository.get_table_by_id(
        table_id=id,
        session=session
    )
    return table
