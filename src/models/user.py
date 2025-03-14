import datetime

from typing import List, TYPE_CHECKING
from sqlalchemy import BIGINT, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.postgres import (
    Base, intpk, created_at, updated_at
)

if TYPE_CHECKING:
    from .cart import Cart
    from .reservation import ReservationDetail
    from .order import Order


class User(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    telegram_id: Mapped[int] = mapped_column(BIGINT, index=True, unique=True)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    username: Mapped[str | None]
    birth_day: Mapped[datetime.datetime | None]
    is_premium: Mapped[bool] = mapped_column(server_default=text("false"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at | None]
    is_active: Mapped[bool] = mapped_column(server_default=text("true"))

    sources: Mapped[List["UserSource"]] = relationship(back_populates="user")
    carts: Mapped['Cart'] = relationship(back_populates="user")
    reservation_details: Mapped['ReservationDetail'] = relationship(
        back_populates="user")
    orders: Mapped['Order'] = relationship(back_populates="user")


class UserSource(Base):
    __tablename__ = "user_sources"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"))
    source_type: Mapped[str] = mapped_column(server_default="direct")
    source_details: Mapped[str | None]
    created_at: Mapped[created_at]

    user: Mapped["User"] = relationship(back_populates="sources")
