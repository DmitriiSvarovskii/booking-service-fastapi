from typing import TYPE_CHECKING
from sqlalchemy import text
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.db.postgres import (
    Base, intpk, str_64,
    created_at, created_by,
    updated_at, updated_by,
    deleted_at, deleted_by, is_deleted,
)

if TYPE_CHECKING:
    from .product import Product
    from .employee import Employee


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[intpk]
    name: Mapped[str_64]
    availability: Mapped[bool] = mapped_column(server_default=text("true"))
    created_by: Mapped[created_by]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    updated_by: Mapped[updated_by | None]
    is_deleted: Mapped[is_deleted]
    deleted_at: Mapped[deleted_at]
    deleted_by: Mapped[deleted_by | None]

    products: Mapped['Product'] = relationship(
        back_populates="category")
    employees: Mapped['Employee'] = relationship(
        back_populates="categories")
