from typing import Optional
from pydantic import BaseModel, ConfigDict
from pydantic.json_schema import SkipJsonSchema


class CartBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: Optional[SkipJsonSchema[int]] = None
    product_id: int
    quantity: Optional[SkipJsonSchema[int]] = 1


class CartCreate(CartBase):
    pass


class CartRemove(CartBase):
    pass


class CartGet(CartBase):
    id: int
    quantity: int


class ProductCart(BaseModel):
    id: int
    name: str
    price: float


class CartAllGet(CartBase):
    id: int
    product: ProductCart
    quantity: int

    @property
    def total_price(self) -> float:
        return self.quantity * self.product.price
