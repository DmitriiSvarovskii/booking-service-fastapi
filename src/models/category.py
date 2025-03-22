from typing import TYPE_CHECKING
from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.db.postgres import (
    Base, intpk, str_64,
    created_at,
    updated_at,
    deleted_at, is_deleted,
)

if TYPE_CHECKING:
    from .product import Product


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[intpk]
    name: Mapped[str_64]
    availability: Mapped[bool] = mapped_column(server_default=text("true"))
    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at | None]
    updated_by: Mapped[int | None] = mapped_column(ForeignKey(
        "employees.id", ondelete="CASCADE"), nullable=True)
    is_deleted: Mapped[is_deleted]
    deleted_at: Mapped[deleted_at | None]
    deleted_by: Mapped[int | None] = mapped_column(ForeignKey(
        "employees.id", ondelete="CASCADE"), nullable=True)

    products: Mapped[list['Product']] = relationship(back_populates="category")
