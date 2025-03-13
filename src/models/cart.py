from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.postgres import Base, intpk

if TYPE_CHECKING:
    from .product import Product
    from .user import User


class Cart(Base):
    __tablename__ = "carts"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"))
    quantity: Mapped[int]

    product_rel: Mapped["Product"] = relationship(
        foreign_keys=[product_id]
    )
    product: Mapped['Product'] = relationship(
        back_populates="cart")
    user: Mapped['User'] = relationship(
        back_populates="cart")
