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
    images: list[ProductImageGet]


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
    products: list[ProductBase]


class ProductGet(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    category: CategoryGet
