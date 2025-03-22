from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_async_session
from src.repositories.assortment import AssortmentRepository
from src.schemas.assortment import AssortmentGet, ProductGet
from src.dependencies.current_user import get_current_user


router = APIRouter(
    prefix="/api/v1/assortment",
    tags=["Assortment"],
    dependencies=[Depends(get_current_user)]

)


@router.get(
    "/",
    response_model=list[AssortmentGet],
    status_code=status.HTTP_200_OK
)
async def get_all_assortment(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Получение всего ассортимента.

    **Требует JWT-токен.**
    Если токен устарел - необходимо передать refresh token.
    """

    assortment_data = await AssortmentRepository.get_all_assortment(
        session=session
    )
    return assortment_data


@router.get(
    "/product/{id}/",
    response_model=ProductGet,
    status_code=status.HTTP_200_OK
)
async def get_one_product(
    product_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Получение информации о конкретном продукте по его ID.

    **Требует JWT-токен.**
    Если токен устарел - необходимо передать refresh token.
    """
    product_data = await AssortmentRepository.get_product_by_id(
        product_id=product_id,
        session=session
    )
    return product_data
