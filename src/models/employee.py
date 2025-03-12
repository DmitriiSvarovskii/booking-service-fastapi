from typing import List
from sqlalchemy import (
    ForeignKey, Table,
    Column, Integer,
    UniqueConstraint, text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.postgres import (
    Base, intpk
)


employees_roles = Table(
    "employees_roles",
    Base.metadata,
    Column("employees_id", Integer, ForeignKey(
        "employees.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", Integer, ForeignKey(
        "roles.id", ondelete="CASCADE"), primary_key=True),
    UniqueConstraint("employee_id", "role_id", name="uq_employee_role")
)


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[intpk]
    full_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(nullable=True, unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    roles: Mapped[List["Role"]] = relationship(
        back_populates="employees"
    )


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=True)
    level: Mapped[int] = mapped_column(
        nullable=False, server_default=text("0"))

    employees: Mapped[List["Employee"]] = relationship(
        secondary=employees_roles, back_populates="roles"
    )
