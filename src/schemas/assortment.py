from typing import List
from pydantic import BaseModel, ConfigDict


class ProductImageGet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str
    is_main: bool


class ProductBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    price: float
    images: List[ProductImageGet]


class CategoryGet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    # description: str


class AssortmentGet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    availability: bool
    products: List[ProductBase]


class ProductGet(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    category: CategoryGet
