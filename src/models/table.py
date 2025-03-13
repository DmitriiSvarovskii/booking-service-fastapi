from typing import List
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.postgres import (
    Base, intpk, str_64, str_256,
    created_at, updated_at,
    deleted_at, is_deleted
)


class Table(Base):
    __tablename__ = "tables"

    id: Mapped[intpk]
    name: Mapped[str_64]
    is_active: Mapped[bool] = mapped_column(server_default=text("true"))
    created_by: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    updated_by: Mapped[int | None] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"))
    is_deleted: Mapped[is_deleted]
    deleted_at: Mapped[deleted_at]
    deleted_by: Mapped[int | None] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"))

    table_info: Mapped['TableInfo'] = relationship(
        back_populates="table")
    images: Mapped[List['TableImage']] = relationship(
        back_populates="product")


class TableInfo(Base):
    __tablename__ = "table_info"

    id: Mapped[intpk]
    table_id: Mapped[str_64]
    description: Mapped[str_256]
    created_by: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    updated_by: Mapped[int | None] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"))
    is_deleted: Mapped[is_deleted]
    deleted_at: Mapped[deleted_at]
    deleted_by: Mapped[int | None] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"))

    table: Mapped['Table'] = relationship(
        back_populates="table_info")


class TableImage(Base):
    __tablename__ = "tsble_images"

    id: Mapped[intpk]
    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id"))
    url: Mapped[str_256]
    is_main: Mapped[bool] = mapped_column(server_default=text("false"))

    table: Mapped['Table'] = relationship(back_populates="images")
