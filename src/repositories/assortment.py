from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Product, Category
from src.schemas.assortment import AssortmentGet, ProductGet
from src.db.postgres import get_async_session
from src.common.db_decorators import handle_db_errors


class AssortmentRepository:
    """Класс для работы с таблицей tables."""
    @staticmethod
    @handle_db_errors
    async def get_all_assortment(
        session: AsyncSession = Depends(get_async_session)
    ) -> List[AssortmentGet]:
        query = (
            select(Category)
            .options(
                selectinload(Category.products)
                .selectinload(Product.images)
            )
            .where(
                Category.availability is not False,
                Category.is_deleted is not True,
                Product.availability is not False,
                Product.is_deleted is not True,
            )
        )
        result = await session.execute(query)
        categories = result.scalars().all()

        return [
            AssortmentGet.model_validate(c).model_dump() for c in categories
        ]

    @staticmethod
    @handle_db_errors
    async def get_product_by_id(
        product_id: int,
        session: AsyncSession = Depends(get_async_session)
    ) -> ProductGet:
        query = (
            select(Product)
            .options(selectinload(Product.category))
            .options(selectinload(Product.images))
            .where(
                Product.id == product_id,
                Category.availability is not False,
                Category.is_deleted is not True,
                Product.availability is not False,
                Product.is_deleted is not True
            )
        )
        result = await session.execute(query)
        product = result.scalar()
        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        return product
