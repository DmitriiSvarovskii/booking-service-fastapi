from typing import Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_async_session
from src.schemas.reservation import ReservationDataCreate, ReservationDataGet
from src.repositories.reservation import ReservationRepository
from src.dependencies.current_user import get_current_user
from src.schemas.auth import AuthUser
from src.docs import reservation_descriptions


router = APIRouter(
    prefix="/api/v1/reservation",
    tags=["Reservation"],
    dependencies=[Depends(get_current_user)]

)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[ReservationDataGet],
    summary=reservation_descriptions.GET_ALL_RESERVATIONS_SUMMARY,
    description=reservation_descriptions.GET_ALL_RESERVATIONS_DESCRIPTION
)
async def get_all_reservations_by_user_id(
    current_user: AuthUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    reservations_data = await ReservationRepository.get_all_reservations_by_user_id(  # noqa
        user_id=current_user.user_id,
        session=session
    )
    return reservations_data


@router.get(
    "/{id}/",
    status_code=status.HTTP_200_OK,
    response_model=ReservationDataGet,
    summary=reservation_descriptions.GET_RESERVATION_BY_ID_SUMMARY,
    description=reservation_descriptions.GET_RESERVATION_BY_ID_DESCRIPTION
)
async def get_reservation_by_id(
    reservation_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    reservation_data = await ReservationRepository.get_reservation_by_id(
        reservation_id=reservation_id,
        session=session
    )
    return reservation_data


@router.post(
    "/",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary=reservation_descriptions.CREATE_RESERVATION_SUMMARY,
    description=reservation_descriptions.CREATE_RESERVATION_DESCRIPTION
)
async def create_reservation(
    reservation_data: ReservationDataCreate,
    session: AsyncSession = Depends(get_async_session)
):
    return await ReservationRepository.create_full_reservation(
        reservation_data=reservation_data,
        session=session
    )


@router.put("/{id}/", response_model=Optional[None])
async def put_reservation(
    session: AsyncSession = Depends(get_async_session)
):
    pass


@router.patch("/{id}/", response_model=Optional[None])
async def patch_reservation(
    session: AsyncSession = Depends(get_async_session)
):
    pass


@router.delete("/{id}/", response_model=Optional[None])
async def delete_reservation(
    session: AsyncSession = Depends(get_async_session)
):
    pass
