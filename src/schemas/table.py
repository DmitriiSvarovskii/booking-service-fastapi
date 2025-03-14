from pydantic import BaseModel, ConfigDict


class TableBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class TableImageBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str
    is_main: bool


class TableInfoBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    description: str


class TableGet(TableBase):
    model_config = ConfigDict(from_attributes=True)

    table_images: list[TableImageBase]
    table_info: TableInfoBase
