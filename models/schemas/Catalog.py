from typing import List

from pydantic import BaseModel


class Account(BaseModel):
    category: str
    name: str
    description: str
    price: float
    uid: str
    count: int


class Catalog(BaseModel):
    accounts: List[Account]


class Message(BaseModel):
    accounts: List[Account]
    status: str


class Response(BaseModel):
    status_code: int
    message: Message
