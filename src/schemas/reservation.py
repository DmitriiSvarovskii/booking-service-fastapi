import datetime

from typing import Optional
from pydantic import BaseModel, ConfigDict
from pydantic.json_schema import SkipJsonSchema

from src.models.reservation import ReservationStatusEnum


class ReservationDetailsCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    reservation_id: Optional[SkipJsonSchema[int]] = None
    table_id: int
    user_id: int
    comment: Optional[str] = None


class ReservationDetailsGet(ReservationDetailsCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ReservationCustomerInfoCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    reservation_id: Optional[SkipJsonSchema[int]] = None
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    phone: Optional[str] = None


class ReservationCustomerInfoGet(ReservationCustomerInfoCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ReservationCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    start_time: datetime.datetime
    end_time: datetime.datetime
    status: Optional[SkipJsonSchema[ReservationStatusEnum]
                     ] = ReservationStatusEnum.PENDING


class ReservationGet(ReservationCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    # status: int


class ReservationDataCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    reservation_data: ReservationCreate
    reservation_details_data: ReservationDetailsCreate
    reservation_customer_info_data: Optional[ReservationCustomerInfoCreate] = None  # noqa


class ReservationDataGet(ReservationGet):
    model_config = ConfigDict(from_attributes=True)

    reservation_details: ReservationDetailsGet
    reservation_customer_info: Optional[ReservationCustomerInfoGet]  # noqa
