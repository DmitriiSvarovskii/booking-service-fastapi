from pydantic import BaseModel


class InitDataRequest(BaseModel):
    init_data: str
