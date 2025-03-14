from typing import List
from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.db.postgres import (
    Base, intpk,
    created_at, created_by,
    updated_at, updated_by,
    deleted_at, deleted_by, is_deleted,
)


class Establishment(Base):
    __tablename__ = "establishments"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str | None]
    address: Mapped[str] = mapped_column(nullable=False)
    route_description: Mapped[str | None]
    greeting_message: Mapped[str | None]
    status: Mapped[bool] = mapped_column(server_default=text("true"))
    is_active: Mapped[bool] = mapped_column(server_default=text("true"))
    created_by: Mapped[created_by]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    updated_by: Mapped[updated_by | None]
    is_deleted: Mapped[is_deleted]
    deleted_at: Mapped[deleted_at]
    deleted_by: Mapped[deleted_by | None]

    working_hours: Mapped[List["WorkingHours"]] = relationship(
        back_populates="establishment")


class WorkingHours(Base):
    __tablename__ = "working_hours"

    id: Mapped[intpk]
    establishment_id: Mapped[int] = mapped_column(
        ForeignKey("establishments.id"), nullable=False)
    day_of_week: Mapped[int] = mapped_column(nullable=False)
    open_time: Mapped[str] = mapped_column(nullable=True)
    close_time: Mapped[str] = mapped_column(nullable=True)

    establishment: Mapped["Establishment"] = relationship(
        back_populates="working_hours")
