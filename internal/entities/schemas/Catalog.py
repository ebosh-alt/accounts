from typing import List, Optional

from pydantic import BaseModel


### TODO: edit logic

class Account(BaseModel):
    category: Optional[str] = None
    subcategory: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    uid: Optional[str] = None
    count: Optional[int] = None


class Catalog(BaseModel):
    accounts: Optional[List[Account]] = []


class Message(BaseModel):
    catalog: List[Account]
    status: str
    detail: str


class Response(BaseModel):
    message: Message
