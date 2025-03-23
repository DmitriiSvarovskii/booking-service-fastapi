from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_async_session
from src.schemas.table import TableGet
# from src.schemas.auth import AuthUser
from src.repositories.table import TableRepository
from src.dependencies.current_user import get_current_user
from src.docs import table_descriptions


router = APIRouter(
    prefix="/table",
    tags=["Table"],
    dependencies=[Depends(get_current_user)]

)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[TableGet],
    summary=table_descriptions.GET_ALL_TABLES_SUMMARY,
    description=table_descriptions.GET_ALL_TABLES_DESCRIPTION
)
async def get_all_table(
    session: AsyncSession = Depends(get_async_session)
):
    tables = await TableRepository.get_all_tables(
        session=session
    )
    return tables


@router.get(
    "/{id}/",
    status_code=status.HTTP_200_OK,
    response_model=TableGet,
    summary=table_descriptions.GET_TABLE_BY_ID_SUMMARY,
    description=table_descriptions.GET_TABLE_BY_ID_DESCRIPTION
)
async def get_table_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session)
):
    table = await TableRepository.get_table_by_id(
        table_id=id,
        session=session
    )
    return table
