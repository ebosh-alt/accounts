from pydantic import BaseModel


class Shop(BaseModel):
    name: str
    host: str
    port: int


