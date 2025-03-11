from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_async_session


router = APIRouter(
    prefix="/api/v1/order",
    tags=["Order"])


@router.get("/", response_model=Optional[None])
async def get_all_order(
    session: AsyncSession = Depends(get_async_session)
):
    pass


@router.get("/{id}/", response_model=Optional[None])
async def get_one_order(
    session: AsyncSession = Depends(get_async_session)
):
    pass


@router.post("/", response_model=Optional[None])
async def post_order(
    session: AsyncSession = Depends(get_async_session)
):
    pass


@router.put("/{id}/", response_model=Optional[None])
async def put_order(
    session: AsyncSession = Depends(get_async_session)
):
    pass


@router.patch("/{id}/", response_model=Optional[None])
async def patch_order(
    session: AsyncSession = Depends(get_async_session)
):
    pass


@router.delete("/{id}/", response_model=Optional[None])
async def delete_order(
    session: AsyncSession = Depends(get_async_session)
):
    pass
