from fastapi import Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_async_session
from src.common.db_decorators import handle_db_errors
from src.models import (
    Reservation, ReservationDetail,
    ReservationCustomerInfo
)
from src.schemas.reservation import (
    ReservationCreate, ReservationDetailsCreate,
    ReservationCustomerInfoCreate, ReservationDataGet,
    ReservationDataCreate
)


class ReservationRepository:
    """Класс для работы с таблицей reservations."""

    @staticmethod
    @handle_db_errors
    async def get_reservation_by_id(
        reservation_id: int,
        session: AsyncSession = Depends(get_async_session)
    ) -> ReservationDataGet:
        query = (
            select(Reservation)
            .options(selectinload(Reservation.reservation_details))
            .options(selectinload(Reservation.reservation_customer_info))
            .where(Reservation.id == reservation_id)
        )
        result = await session.execute(query)
        reservation = result.scalar()

        if reservation is None:
            raise HTTPException(
                status_code=404,
                detail="Reservation not found"
            )

        return reservation

    @staticmethod
    @handle_db_errors
    async def get_all_reservations_by_user_id(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)
    ) -> list[ReservationDataGet]:
        query = (
            select(Reservation)
            .options(selectinload(Reservation.reservation_details))
            .options(selectinload(Reservation.reservation_customer_info))
            .join(ReservationDetail)
            .where(ReservationDetail.user_id == user_id)
            .order_by(Reservation.start_time)
        )
        result = await session.execute(query)
        reservations = result.scalars().all()
        return reservations

    @staticmethod
    @handle_db_errors
    async def create_reservation(
        reservation_data: ReservationCreate,
        session: AsyncSession = Depends(get_async_session)
    ):
        stmt = (
            insert(Reservation)
            .values(**reservation_data.model_dump())
            .returning(Reservation.id)
        )
        result = await session.execute(stmt)
        return result.scalars().one()

    @staticmethod
    @handle_db_errors
    async def create_reservation_details(
        reservation_details_data: ReservationDetailsCreate,
        session: AsyncSession = Depends(get_async_session)
    ):
        stmt = (
            insert(ReservationDetail)
            .values(**reservation_details_data.model_dump())
        )
        await session.execute(stmt)
        return {"status": "success"}

    @staticmethod
    @handle_db_errors
    async def create_reservation_customer_info(
        reservation_customer_info_data: ReservationCustomerInfoCreate,
        session: AsyncSession = Depends(get_async_session)
    ):
        stmt = (
            insert(ReservationCustomerInfo)
            .values(**reservation_customer_info_data.model_dump())
        )
        await session.execute(stmt)
        return {"status": "success"}

    @classmethod
    @handle_db_errors
    async def create_full_reservation(
        cls,
        reservation_data: ReservationDataCreate,
        session: AsyncSession
    ) -> dict:
        """Создает бронирование, детали и данные клиента (если есть)."""
        async with session.begin():
            try:
                reservation_id = await cls.create_reservation(
                    reservation_data=reservation_data.reservation_data,
                    session=session
                )

                reservation_data.reservation_details_data.reservation_id = reservation_id  # noqa
                await cls.create_reservation_details(
                    reservation_details_data=reservation_data.reservation_details_data,  # noqa
                    session=session
                )

                if reservation_data.reservation_customer_info_data:
                    reservation_data.reservation_customer_info_data.reservation_id = reservation_id  # noqa
                    await cls.create_reservation_customer_info(
                        reservation_customer_info_data=reservation_data.reservation_customer_info_data,  # noqa
                        session=session
                    )

                return {"status": "success"}

            except HTTPException as e:
                raise e
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Unexpected error: {str(e)}")
