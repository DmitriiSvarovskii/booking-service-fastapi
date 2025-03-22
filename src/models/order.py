from typing import TYPE_CHECKING
from enum import Enum
from sqlalchemy import ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship


from src.db.postgres import (
    Base, intpk,
    created_at, updated_at
)

if TYPE_CHECKING:
    from .user import User
    from .product import Product
    from .reservation import Reservation


class OrderStatusEnum(Enum):
    PENDING = 1
    CONFIRMED = 2
    CANCELED = 3
    COMPLETED = 4


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"))
    reservation_id: Mapped[int] = mapped_column(
        ForeignKey("reservations.id", ondelete="CASCADE"))
    comment: Mapped[str | None]
    status: Mapped[OrderStatusEnum] = mapped_column(
        SQLEnum(OrderStatusEnum),
        nullable=False,
        default=OrderStatusEnum.PENDING
    )
    total_price: Mapped[float]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at | None]

    user: Mapped['User'] = relationship(back_populates="orders")
    reservation: Mapped['Reservation'] = relationship(
        back_populates="orders")
    order_details: Mapped[list['OrderDetail']] = relationship(
        back_populates="orders")


class OrderDetail(Base):
    __tablename__ = "order_details"

    id: Mapped[intpk]
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"))
    quantity: Mapped[int]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at | None]

    orders: Mapped['Order'] = relationship(
        back_populates="order_details")
    product: Mapped['Product'] = relationship(
        back_populates="order_details")
