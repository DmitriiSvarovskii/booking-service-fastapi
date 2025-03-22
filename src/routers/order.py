from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_async_session
from src.schemas.order import OrderCreate, OrderDataGet
from src.schemas.auth import AuthUser
from src.repositories.order import OrderRepository
from src.services.order_service import OrderService
from src.dependencies.current_user import get_current_user


router = APIRouter(
    prefix="/api/v1/order",
    tags=["Order"],
    dependencies=[Depends(get_current_user)]

)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[OrderDataGet]
)
async def get_all_orders(
    current_user: AuthUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Получение всех оформленных заказов текущего пользователя.

    **Требует JWT-токен.**
    Если токен устарел - необходимо передать refresh token.
    """
    orders_data = await OrderRepository.get_all_orders_by_user_id(
        user_id=current_user.user_id,
        session=session
    )
    return orders_data


@router.get(
    "/{id}/",
    status_code=status.HTTP_200_OK,
    response_model=OrderDataGet
)
async def get_order_by_order_id(
    order_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Получение одного заказа текущего пользователя.

    **Требует JWT-токен.**
    Если токен устарел - необходимо передать refresh token.
    """
    order_data = await OrderRepository.get_order_by_id(
        order_id=order_id,
        session=session
    )
    return order_data


@router.post(
    "/",
    response_model=dict,
    status_code=status.HTTP_201_CREATED
)
async def post_order(
    order_data: OrderCreate,
    session: AsyncSession = Depends(get_async_session)
):
    return await OrderService.create_order_from_cart(
        order_data=order_data,
        session=session
    )
