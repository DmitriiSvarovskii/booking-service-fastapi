from typing import Optional, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_async_session


router = APIRouter(
    prefix="/api/v1/cart",
    tags=["Cart"])


@router.get("/", response_model=List[None])
async def get_all_cart(
    session: AsyncSession = Depends(get_async_session)
):
    pass


@router.post("/", response_model=Optional[None])
async def post_cart(
    session: AsyncSession = Depends(get_async_session)
):
    pass


@router.put("/{id}/", response_model=Optional[None])
async def put_cart(
    session: AsyncSession = Depends(get_async_session)
):
    pass


@router.patch("/{id}/", response_model=Optional[None])
async def patch_cart(
    session: AsyncSession = Depends(get_async_session)
):
    pass


@router.delete("/{id}/", response_model=Optional[None])
async def delete_one_item(
    session: AsyncSession = Depends(get_async_session)
):
    pass


@router.delete("/", response_model=Optional[None])
async def delete_all_cart(
    session: AsyncSession = Depends(get_async_session)
):
    pass
