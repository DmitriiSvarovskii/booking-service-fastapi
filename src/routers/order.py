from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_async_session
from src.schemas.order import OrderCreate, OrderDataGet
from src.schemas.auth import AuthUser
from src.repositories.order import OrderRepository
from src.services.order_service import OrderService
from src.dependencies.current_user import get_current_user
from src.docs import order_descriptions


router = APIRouter(
    prefix="/api/v1/order",
    tags=["Order"],
    dependencies=[Depends(get_current_user)]

)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[OrderDataGet],
    summary=order_descriptions.GET_ALL_ORDERS_SUMMARY,
    description=order_descriptions.GET_ALL_ORDERS_DESCRIPTION
)
async def get_all_orders(
    current_user: AuthUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    orders_data = await OrderRepository.get_all_orders_by_user_id(
        user_id=current_user.user_id,
        session=session
    )
    return orders_data


@router.get(
    "/{id}/",
    status_code=status.HTTP_200_OK,
    response_model=OrderDataGet,
    summary=order_descriptions.GET_ORDER_BY_ID_SUMMARY,
    description=order_descriptions.GET_ORDER_BY_ID_SUMMARY
)
async def get_order_by_id(
    order_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    order_data = await OrderRepository.get_order_by_id(
        order_id=order_id,
        session=session
    )
    return order_data


@router.post(
    "/",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary=order_descriptions.CREATE_ORDER_SUMMARY,
    description=order_descriptions.CREATE_ORDER_DESCRIPTION
)
async def create_order(
    order_data: OrderCreate,
    session: AsyncSession = Depends(get_async_session)
):
    return await OrderService.create_order_from_cart(
        order_data=order_data,
        session=session
    )
