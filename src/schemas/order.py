from typing import Optional
from pydantic import BaseModel, ConfigDict
from pydantic.json_schema import SkipJsonSchema

from src.models.order import OrderStatusEnum


class OrderDetailsCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: Optional[SkipJsonSchema[int]] = None
    product_id: int
    quantity: int


class OrderDetailsGet(OrderDetailsCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class OrderCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    reservation_id: int
    comment: Optional[str] = None
    status: Optional[SkipJsonSchema[OrderStatusEnum]
                     ] = OrderStatusEnum.PENDING
    total_price: Optional[SkipJsonSchema[float]] = None


class OrderGet(OrderCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    # status: int


class OrderDataCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_data: OrderCreate
    order_details_data: list[OrderDetailsCreate]


class OrderDataGet(OrderGet):
    model_config = ConfigDict(from_attributes=True)

    order_details: list[OrderDetailsGet]
