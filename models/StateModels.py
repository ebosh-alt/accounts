from pydantic import BaseModel


class Score(BaseModel):
    user_id: int | None
    amount: float
    guarantor: bool
    is_payment: bool


class Account(BaseModel):
    id_account: int
    score: Score


class ShoppingCart(BaseModel):
    shop: str | None = None
    name: str | None = None
    price: float | None = None
    description: str | None = None
    count: int = 1
    guarantor: bool | None = None
    message_id: int | None = None
    deals_id: list = []
    accounts_id: list = []
    uuid: str | None = None


class Deal(BaseModel):
    user_id: int = None
    shop: str = None
    price: int = None
    description: str = None
    data: str = None
    name: str = None
    guarant_type: bool = None
