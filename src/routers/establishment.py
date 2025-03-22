from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_async_session
from src.dependencies.current_user import get_current_user


router = APIRouter(
    prefix="/api/v1/establishment",
    tags=["Establishment"],
    dependencies=[Depends(get_current_user)]

)


@router.get("/", response_model=list[None])
async def get_establishment_info(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Получение информации о заведении.

    **Требует JWT-токен.**
    Если токен устарел - необходимо передать refresh token.
    """
    pass
