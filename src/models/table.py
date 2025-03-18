from typing import List, TYPE_CHECKING
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.postgres import (
    Base, intpk, str_64, str_256,
    created_at, updated_at,
    deleted_at, is_deleted
)

if TYPE_CHECKING:
    from .reservation import ReservationDetail


class Table(Base):
    __tablename__ = "tables"

    id: Mapped[intpk]
    name: Mapped[str_64]
    is_active: Mapped[bool] = mapped_column(server_default=text("true"))
    created_by: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at | None]
    updated_by: Mapped[int | None] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"))
    is_deleted: Mapped[is_deleted]
    deleted_at: Mapped[deleted_at]
    deleted_by: Mapped[int | None] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"))

    table_images: Mapped[List['TableImage']] = relationship(
        "TableImage", back_populates="table")
    table_info: Mapped['TableInfo'] = relationship(
        "TableInfo", back_populates="table")
    reservation_details: Mapped['ReservationDetail'] = relationship(
        back_populates="table")


class TableInfo(Base):
    __tablename__ = "table_info"

    id: Mapped[intpk]
    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id"))
    description: Mapped[str_256]
    created_by: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at | None]
    updated_by: Mapped[int | None] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"))
    is_deleted: Mapped[is_deleted]
    deleted_at: Mapped[deleted_at]
    deleted_by: Mapped[int | None] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"))

    table: Mapped['Table'] = relationship("Table", back_populates="table_info")


class TableImage(Base):
    __tablename__ = "table_images"

    id: Mapped[intpk]
    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id"))
    url: Mapped[str_256]
    is_main: Mapped[bool] = mapped_column(server_default=text("false"))

    table: Mapped['Table'] = relationship(
        "Table", back_populates="table_images")
