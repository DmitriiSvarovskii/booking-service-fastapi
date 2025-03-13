import datetime

from decimal import Decimal
from typing import TYPE_CHECKING, List
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey, Numeric, func, text

from src.db.postgres import (
    Base, intpk, str_64, str_256,
    created_at, created_by,
    updated_at, updated_by,
    deleted_at, deleted_by, is_deleted,
)

if TYPE_CHECKING:
    from .category import Category
    from .cart import Cart


class ProductImage(Base):
    __tablename__ = "product_images"

    id: Mapped[intpk]
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    url: Mapped[str_256]
    is_main: Mapped[bool] = mapped_column(server_default=text("false"))

    product: Mapped['Product'] = relationship(back_populates="images")


class ProductPriceHistory(Base):
    __tablename__ = "product_price_histories"

    id: Mapped[intpk]
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    changed_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now())

    product: Mapped['Product'] = relationship(back_populates="price_history")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[intpk]
    name: Mapped[str_64]
    description: Mapped[str_256 | None]
    availability: Mapped[bool] = mapped_column(server_default=text("true"))
    created_by: Mapped[created_by]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    updated_by: Mapped[updated_by | None]
    is_deleted: Mapped[is_deleted]
    deleted_at: Mapped[deleted_at]
    deleted_by: Mapped[deleted_by | None]

    category: Mapped['Category'] = relationship(
        back_populates="products")
    cart: Mapped['Cart'] = relationship(
        back_populates="product")
    images: Mapped[List['ProductImage']] = relationship(
        back_populates="product")
    price_history: Mapped[List['ProductPriceHistory']
                          ] = relationship(back_populates="product")
