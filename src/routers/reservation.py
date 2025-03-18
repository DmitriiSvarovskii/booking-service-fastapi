from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_async_session
from src.schemas.reservation import ReservationDataCreate, ReservationDataGet
from src.repositories.reservation import ReservationRepository

router = APIRouter(
    prefix="/api/v1/reservation",
    tags=["Reservation"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[ReservationDataGet]
)
async def get_all_reservation(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    reservations_data = await ReservationRepository.get_all_reservation_by_user(  # noqa
        user_id=user_id,  # noqa
        session=session
    )
    return reservations_data


@router.get(
    "/{id}/",
    status_code=status.HTTP_200_OK,
    response_model=ReservationDataGet
)
async def get_one_reservation(
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
    status_code=status.HTTP_201_CREATED
)
async def post_reservation(
    reservation_data: ReservationDataCreate,
    session: AsyncSession = Depends(get_async_session)
):
    async with session.begin():
        try:
            reservation_id = await ReservationRepository.create_reservation(
                reservation_data=reservation_data.reservation_data,
                session=session
            )
            reservation_details_data = reservation_data.reservation_details_data  # noqa
            reservation_details_data.reservation_id = reservation_id

            if reservation_data.reservation_customer_info_data:
                reservation_customer_info_data = reservation_data.reservation_customer_info_data  # noqa
                reservation_customer_info_data.reservation_id = reservation_id  # noqa

            await ReservationRepository.create_reservation_details(
                reservation_details_data=reservation_details_data,
                session=session
            )
            await ReservationRepository.create_reservation_customer_info(
                reservation_customer_info_data=reservation_customer_info_data,  # noqa
                session=session
            )

            return {"status": "success"}

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Unexpected error: {str(e)}")


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
