from enum import Enum
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from src.db.postgres import (
    Base, intpk, str_64
)


class EmployeeRoleEnum(Enum):
    MANAGER = 1
    ADMIN = 2
    SUPERADMIN = 3


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[intpk]
    first_name: Mapped[str_64 | None]
    last_name: Mapped[str_64 | None]
    phone: Mapped[str_64 | None] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[EmployeeRoleEnum] = mapped_column(
        SQLEnum(EmployeeRoleEnum),
        nullable=False,
        default=EmployeeRoleEnum.MANAGER
    )
