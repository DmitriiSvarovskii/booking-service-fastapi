import datetime

from enum import Enum
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.postgres import (
    Base, intpk, created_at, changed_at,
    updated_at, changed_by
)

if TYPE_CHECKING:
    from .user import User
    from .order import Order
    from .table import Table


class ReservationStatusEnum(Enum):
    PENDING = 1
    CONFIRMED = 2
    CANCELED = 3
    COMPLETED = 4


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[intpk]
    status: Mapped[ReservationStatusEnum] = mapped_column(
        SQLEnum(ReservationStatusEnum),
        nullable=False,
        default=ReservationStatusEnum.PENDING
    )
    start_time: Mapped[datetime.datetime]
    end_time: Mapped[datetime.datetime]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at | None]

    reservation_details: Mapped['ReservationDetail'] = relationship(
        back_populates="reservation")
    status_history: Mapped[list["ReservationStatusHistory"]] = relationship(
        back_populates="reservation", cascade="all, delete-orphan"
    )
    review: Mapped['ReservationReview'] = relationship(
        back_populates="reservation")
    reservation_customer_info: Mapped[
        'ReservationCustomerInfo'
    ] = relationship(back_populates="reservation")
    orders: Mapped['Order'] = relationship(
        back_populates="reservation")


class ReservationStatusHistory(Base):
    __tablename__ = "reservation_status_histories"

    id: Mapped[intpk]
    reservation_id: Mapped[int] = mapped_column(
        ForeignKey("reservations.id", ondelete="CASCADE"), nullable=False
    )
    previous_status: Mapped[ReservationStatusEnum] = mapped_column(
        SQLEnum(ReservationStatusEnum), nullable=True
    )
    new_status: Mapped[ReservationStatusEnum] = mapped_column(
        SQLEnum(ReservationStatusEnum), nullable=False
    )
    changed_by: Mapped[changed_by]
    changed_at: Mapped[changed_at]

    reservation: Mapped["Reservation"] = relationship(
        back_populates="status_history")


class ReservationDetail(Base):
    __tablename__ = "reservation_details"

    id: Mapped[intpk]
    reservation_id: Mapped[int] = mapped_column(
        ForeignKey("reservations.id", ondelete="CASCADE")
    )
    table_id: Mapped[int] = mapped_column(
        ForeignKey("tables.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"))
    comment: Mapped[str | None]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at | None]

    user: Mapped['User'] = relationship(back_populates="reservation_details")
    table: Mapped['Table'] = relationship(
        back_populates="reservation_details")
    reservation: Mapped['Reservation'] = relationship(
        back_populates="reservation_details")


class ReservationCustomerInfo(Base):
    __tablename__ = "reservation_customer_infos"

    id: Mapped[intpk]
    reservation_id: Mapped[int] = mapped_column(
        ForeignKey("reservations.id", ondelete="CASCADE"))
    last_name: Mapped[str | None]
    first_name: Mapped[str | None]
    phone: Mapped[str | None]

    reservation: Mapped['Reservation'] = relationship(
        back_populates="reservation_customer_info")


class ReservationReview(Base):
    __tablename__ = "reservation_reviews"

    id: Mapped[intpk]
    reservation_id: Mapped[int] = mapped_column(
        ForeignKey("reservations.id", ondelete="CASCADE"))
    rating: Mapped[float]
    comment: Mapped[str | None]
    created_at: Mapped[created_at]

    reservation: Mapped['Reservation'] = relationship(back_populates="review")
