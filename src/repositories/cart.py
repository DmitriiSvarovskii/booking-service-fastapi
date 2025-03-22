from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from fastapi import Depends, HTTPException

from src.models import Cart
from src.schemas.cart import CartCreate, CartRemove, CartGet, CartAllGet
from src.common.db_decorators import handle_db_errors
from src.db.postgres import get_async_session


class CartRepository:
    @staticmethod
    @handle_db_errors
    async def get_cart_items(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)
    ) -> list[CartAllGet]:
        query = (
            select(Cart)
            .options(selectinload(Cart.product))
            .where(Cart.user_id == user_id)
        )
        result = await session.execute(query)
        cart = result.scalars().all()

        if cart is None:
            raise HTTPException(
                status_code=404,
                detail="Reservation not found"
            )

        return cart

    @staticmethod
    @handle_db_errors
    async def add_one_item_from_cart(
        cart_data: CartCreate,
        session: AsyncSession = Depends(get_async_session)
    ) -> CartGet:
        result = await session.execute(
            select(Cart).where(Cart.user_id == cart_data.user_id,
                               Cart.product_id == cart_data.product_id)
        )
        cart_item = result.scalars().first()

        if cart_item:
            cart_item.quantity += 1
        else:
            cart_item = Cart(**cart_data.model_dump())
            session.add(cart_item)

        await session.commit()
        await session.refresh(cart_item)
        return cart_item

    @staticmethod
    @handle_db_errors
    async def remove_from_cart(
        cart_data: CartRemove,
        session: AsyncSession = Depends(get_async_session)
    ) -> CartGet:
        """
        Уменьшает количество товара в корзине.
        Если количество товара становится 0, удаляет товар из корзины.
        """
        result = await session.execute(
            select(Cart).where(
                Cart.user_id == cart_data.user_id,
                Cart.product_id == cart_data.product_id
            )
        )
        cart_item = result.scalars().first()

        if not cart_item:
            raise HTTPException(
                status_code=404, detail="Item not found in cart")

        if cart_item.quantity > 1:
            print(cart_item.quantity)
            cart_item.quantity -= 1
            print(cart_item.quantity)
        else:
            await session.delete(cart_item)

        await session.commit()
        await session.refresh(cart_item)
        return cart_item

    @staticmethod
    @handle_db_errors
    async def remove_all_from_cart_by_user_id(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)
    ) -> dict:
        """
        Удаляет все товары из корзины для заданного user_id.
        """
        await session.execute(
            delete(Cart)
            .where(Cart.user_id == user_id)
        )

        await session.commit()
        return {"status": "success"}
