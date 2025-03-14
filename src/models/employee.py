from sqlalchemy import (
    ForeignKey, text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.postgres import (
    Base, intpk
)


class EmployeeRole(Base):
    __tablename__ = "employees_roles"

    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"), primary_key=True
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True
    )

    employee: Mapped['Employee'] = relationship(back_populates="roles")
    roles: Mapped['Role'] = relationship(back_populates="employees")


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[intpk]
    full_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(nullable=True, unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    roles: Mapped['EmployeeRole'] = relationship(back_populates="employee")


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=True)
    level: Mapped[int] = mapped_column(
        nullable=False, server_default=text("0")
    )

    employees: Mapped["EmployeeRole"] = relationship(back_populates="roles")
