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
    deal_id: int | None = None
    accounts_id: list = []
    tracker_id: str | None = None
    payment: bool | None = False


class Deal(BaseModel):
    id: int = None
    user_id: int = None
    shop: str = None
    price: int = None
    description: str = None
    data: str = None
    name: str = None
    guarant_type: bool = None
