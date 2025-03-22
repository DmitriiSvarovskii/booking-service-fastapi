from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_async_session
from src.schemas.cart import CartCreate, CartAllGet, CartGet, CartRemove
from src.repositories.cart import CartRepository
from src.dependencies.current_user import get_current_user
from src.schemas.auth import AuthUser
from src.docs import cart_descriptions


router = APIRouter(
    prefix="/api/v1/cart",
    tags=["Cart"],
)


@router.get("/", response_model=list[CartAllGet])
async def get_cart_items(
    session: AsyncSession = Depends(get_async_session),
    current_user: AuthUser = Depends(
        get_current_user),
):
    """
    Получение всех товаров в корзине текущего пользователя.

    **Требует JWT-токен.**
    Если токен устарел - необходимо передать refresh token.
    """
    return await CartRepository.get_cart_items(
        user_id=current_user.user_id,
        session=session
    )


@router.post(
    "/",
    response_model=CartGet,
    status_code=status.HTTP_201_CREATED
)
async def add_one_item_from_cart(
    cart_data: CartCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: AuthUser = Depends(get_current_user),
):
    """
    Добавление товара в корзину.

    **Требует JWT-токен.**
    Если токен устарел - необходимо передать refresh token.
    """
    try:
        cart_data.user_id = current_user.user_id
        return await CartRepository.add_one_item_from_cart(cart_data, session)
    except Exception as e:
        print(f"Error while adding to cart: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Internal error: {str(e)}"
        )


@router.patch(
    "/",
    response_model=CartGet,
    status_code=status.HTTP_200_OK,
    summary=cart_descriptions.REMOVE_ONE_ITEM_FROM_CART_SUMMARY,
    description=cart_descriptions.REMOVE_ONE_ITEM_FROM_CART_DESCRIPTION,
)
async def remove_one_item_from_cart(
    cart_data: CartRemove,
    session: AsyncSession = Depends(get_async_session),
    current_user: AuthUser = Depends(get_current_user),
):
    cart_data.user_id = current_user.user_id
    return await CartRepository.remove_from_cart(cart_data, session)


@router.delete(
    "/all_item/",
    status_code=status.HTTP_200_OK,
    response_model=dict
)
async def remove_all_item_from_cart(
    session: AsyncSession = Depends(get_async_session),
    current_user: AuthUser = Depends(get_current_user),
):
    """
    Очистка всей корзины текущего пользователя.

    **Требует JWT-токен.**
    Если токен устарел - необходимо передать refresh token.
    """
    return await CartRepository.remove_all_from_cart_by_user_id(
        user_id=current_user.user_id,
        session=session
    )
