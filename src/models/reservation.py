import datetime

from typing import TYPE_CHECKING, List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.postgres import (
    Base, intpk, str_64,
    created_at, created_by,
    updated_at, updated_by,
    deleted_at, deleted_by, is_deleted,
)

if TYPE_CHECKING:
    from .user import User
    from .order import Order


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[intpk]
    status: Mapped[int] = mapped_column(
        ForeignKey("reservation_status.id", ondelete="CASCADE"))
    start_time: Mapped[datetime.datetime]
    end_time: Mapped[datetime.datetime]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    reservation_status: Mapped['ReservationStatus'] = relationship(
        back_populates="reservations")
    reservation_details: Mapped[List['ReservationDetail']] = relationship(
        back_populates="reservation")


class ReservationStatus(Base):
    __tablename__ = "reservation_status"

    id: Mapped[intpk]
    name: Mapped[str_64] = mapped_column(unique=True, nullable=False)
    created_at: Mapped[created_at]
    created_by: Mapped[created_by | None]
    updated_at: Mapped[updated_at]
    updated_by: Mapped[updated_by | None]
    is_deleted: Mapped[is_deleted]
    deleted_at: Mapped[deleted_at]
    deleted_by: Mapped[deleted_by | None]

    reservations: Mapped['Reservation'] = relationship(
        back_populates="reservation_status")


class ReservationDetail(Base):
    __tablename__ = "reservation_details"

    id: Mapped[intpk]
    table_id: Mapped[int] = mapped_column(
        ForeignKey("tables.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"))
    comment: Mapped[str | None]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    user: Mapped['User'] = relationship(back_populates="reservation_details")
    orders: Mapped['Order'] = relationship(
        back_populates="reservation_details")


class ReservationCustomerInfo(Base):
    __tablename__ = "reservation_customer_info"

    id: Mapped[intpk]
    reservation_id: Mapped[int] = mapped_column(
        ForeignKey("reservation.id", ondelete="CASCADE"))
    last_name: Mapped[str | None]
    first_name: Mapped[str | None]
    phone: Mapped[str | None]

    reservation: Mapped['Order'] = relationship(
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
