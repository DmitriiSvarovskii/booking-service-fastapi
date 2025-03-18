from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_async_session
from src.repositories.assortment import AssortmentRepository
from src.schemas.assortment import AssortmentGet, ProductGet


router = APIRouter(
    prefix="/api/v1/assortment",
    tags=["Assortment"])


@router.get("/", response_model=List[AssortmentGet])
async def get_all_assortment(
    session: AsyncSession = Depends(get_async_session)
):
    assortment_data = await AssortmentRepository.get_all_assortment(
        session=session
    )
    return assortment_data


@router.get("/product/{id}/", response_model=ProductGet)
async def get_one_product(
    product_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    product_data = await AssortmentRepository.get_product_by_id(
        product_id=product_id,
        session=session
    )
    return product_data
