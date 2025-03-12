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
    from .product import Product


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"))
    reservation_id: Mapped[int] = mapped_column(
        ForeignKey("reservations.id", ondelete="CASCADE"))
    status: Mapped[int] = mapped_column(
        ForeignKey("order_status.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    user: Mapped['User'] = relationship(back_populates="orders")
    reservation: Mapped['OrderDetail'] = relationship(
        back_populates="order")
    order_status: Mapped['OrderStatus'] = relationship(
        back_populates="order")
    order_details: Mapped[List['OrderDetail']] = relationship(
        back_populates="orders")


class OrderStatus(Base):
    __tablename__ = "order_status"

    id: Mapped[intpk]
    name: Mapped[str_64]
    created_at: Mapped[created_at]
    created_by: Mapped[created_by | None]
    updated_at: Mapped[updated_at]
    updated_by: Mapped[updated_by | None]
    is_deleted: Mapped[is_deleted]
    deleted_at: Mapped[deleted_at]
    deleted_by: Mapped[deleted_by | None]

    orders: Mapped[List['Order']] = relationship(back_populates="order_status")


class OrderDetail(Base):
    __tablename__ = "order_details"

    id: Mapped[intpk]
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"))
    quantity: Mapped[int]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    order: Mapped['Order'] = relationship(
        back_populates="order_details")
    product: Mapped['Product'] = relationship(
        back_populates="order_details")
