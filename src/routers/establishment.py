from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_async_session
from src.dependencies.current_user import get_current_user
from src.docs import establishment_descriptions


router = APIRouter(
    prefix="/api/v1/establishment",
    tags=["Establishment"],
    dependencies=[Depends(get_current_user)]

)


@router.get(
    "/",
    response_model=list[None],
    summary=establishment_descriptions.GET_ESTABLISHMENT_BY_ID_SUMMARY,
    description=establishment_descriptions.GET_ESTABLISHMENT_BY_ID_DESCRIPTION
)
async def get_establishment_info(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Получение информации о заведении.

    **Требует JWT-токен.**
    Если токен устарел - необходимо передать refresh token.
    """
    pass
