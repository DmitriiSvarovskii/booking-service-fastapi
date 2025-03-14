from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Table
from src.schemas.table import TableGet
from src.db.postgres import get_async_session
from src.common.db_decorators import handle_db_errors


class TableRepository:
    """Класс для работы с таблицей tables."""

    @staticmethod
    @handle_db_errors
    async def get_table_by_id(
        table_id: int,
        session: AsyncSession = Depends(get_async_session)
    ) -> TableGet:
        query = (
            select(Table)
            .options(selectinload(Table.table_images))
            .options(selectinload(Table.table_info))
            .where(
                Table.id == table_id,
                Table.is_active is not False,
                Table.is_deleted is not True,
            )
            .order_by(Table.name)
        )
        result = await session.execute(query)
        table = result.scalar()

        if table is None:
            raise HTTPException(
                status_code=404,
                detail="Table not found"
            )

        return table

    @staticmethod
    @handle_db_errors
    async def get_all_table(
        session: AsyncSession = Depends(get_async_session)
    ) -> List[TableGet]:
        query = (
            select(Table)
            .options(selectinload(Table.table_images))
            .options(selectinload(Table.table_info))
            .where(
                Table.is_active is not False,
                Table.is_deleted is not True,
            )
            .order_by(Table.name)
        )
        result = await session.execute(query)
        table = result.scalars().all()
        return table
