import datetime

from typing import TYPE_CHECKING, List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.postgres import (
    Base, intpk, str_64, created_at, changed_at,
    updated_at, changed_by, deleted_at,
)

if TYPE_CHECKING:
    from .user import User
    from .order import Order
    from .table import Table


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[intpk]
    status: Mapped[int] = mapped_column(
        ForeignKey("reservation_statuses.id", ondelete="CASCADE"))
    start_time: Mapped[datetime.datetime]
    end_time: Mapped[datetime.datetime]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    reservation_status: Mapped['ReservationStatus'] = relationship(
        back_populates="reservations")

    reservation_details: Mapped['ReservationDetail'] = relationship(
        back_populates="reservation")
    status_history: Mapped[List["ReservationStatusHistory"]] = relationship(
        back_populates="reservation", cascade="all, delete-orphan"
    )
    review: Mapped['ReservationReview'] = relationship(
        back_populates="reservation")
    reservation_customer_info: Mapped['ReservationCustomerInfo'] = relationship(  # noqa
        back_populates="reservation")
    orders: Mapped['Order'] = relationship(
        back_populates="reservation")


class ReservationStatus(Base):
    __tablename__ = "reservation_statuses"

    id: Mapped[intpk]
    name: Mapped[str_64] = mapped_column(unique=True, nullable=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    deleted_at: Mapped[deleted_at]

    reservations: Mapped['Reservation'] = relationship(
        back_populates="reservation_status")


class ReservationStatusHistory(Base):
    __tablename__ = "reservation_status_histories"

    id: Mapped[intpk]
    reservation_id: Mapped[int] = mapped_column(
        ForeignKey("reservations.id", ondelete="CASCADE"), nullable=False
    )
    previous_status: Mapped[int] = mapped_column(
        ForeignKey("reservation_statuses.id", ondelete="SET NULL"),
        nullable=True
    )
    new_status: Mapped[int] = mapped_column(
        ForeignKey("reservation_statuses.id", ondelete="CASCADE"),
        nullable=False
    )
    changed_by: Mapped[changed_by]
    changed_at: Mapped[changed_at]

    reservation: Mapped["Reservation"] = relationship(
        back_populates="status_history")
    reservation_status: Mapped["ReservationStatus"] = relationship(
        foreign_keys=[previous_status])
    new_status_rel: Mapped["ReservationStatus"] = relationship(
        foreign_keys=[new_status])


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
    updated_at: Mapped[updated_at]

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
