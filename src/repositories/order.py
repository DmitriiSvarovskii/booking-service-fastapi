from fastapi import Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_async_session
from src.common.db_decorators import handle_db_errors
from src.models import (
    Order, OrderDetail
)
from src.schemas.order import (
    OrderCreate, OrderDetailsCreate,
    OrderDataGet, OrderDataCreate
)


class OrderRepository:
    """Класс для работы с таблицей orders."""

    @staticmethod
    @handle_db_errors
    async def get_order_by_id(
        order_id: int,
        session: AsyncSession = Depends(get_async_session)
    ) -> OrderDataGet:
        query = (
            select(Order)
            .options(selectinload(Order.order_details))
            .where(Order.id == order_id)
        )
        result = await session.execute(query)
        order = result.scalar()

        if order is None:
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )

        return order

    @staticmethod
    @handle_db_errors
    async def get_all_orders_by_user_id(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)
    ) -> list[OrderDataGet]:
        query = (
            select(Order)
            .options(selectinload(Order.order_details))
            .where(Order.user_id == user_id)
            .order_by(Order.id.desc())
        )
        result = await session.execute(query)
        orders = result.scalars().all()
        return orders

    @staticmethod
    @handle_db_errors
    async def create_order(
        order_data: OrderCreate,
        session: AsyncSession = Depends(get_async_session)
    ):
        stmt = (
            insert(Order)
            .values(**order_data.model_dump())
            .returning(Order.id)
        )
        result = await session.execute(stmt)
        return result.scalars().one()

    @staticmethod
    @handle_db_errors
    async def create_order_details(
        order_details_list: list[OrderDetailsCreate],
        session: AsyncSession = Depends(get_async_session)
    ):
        """
        Вставляет сразу несколько записей в таблицу OrderDetail,
        используя Pydantic-модели напрямую.
        """
        if not order_details_list:
            return {"status": "error", "message": "Empty order details list"}

        stmt = insert(OrderDetail).values(
            [order.model_dump() for order in order_details_list])

        await session.execute(stmt)
        await session.commit()

        return {"status": "success"}

    @classmethod
    @handle_db_errors
    async def create_full_orders(
        cls,
        order_data: OrderDataCreate,
        session: AsyncSession
    ) -> dict:
        """Создает бронирование, детали и данные клиента (если есть)."""
        async with session.begin():
            try:
                order_id = await cls.create_order(
                    order_data=order_data.order_data,
                    session=session
                )
                order_details_with_id = [
                    order_details.model_copy(update={"order_id": order_id})
                    for order_details in order_data.order_details_data
                ]
                await cls.create_order_details(
                    order_details_data=order_details_with_id,
                    session=session
                )

                return {"status": "success"}

            except HTTPException as e:
                raise e
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Unexpected error: {str(e)}")
