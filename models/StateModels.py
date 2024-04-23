from pydantic import BaseModel


class Score(BaseModel):
    user_id: int | None
    amount: float
    guarantor: bool
    is_payment: bool


class Account(BaseModel):
    id_account: int
    score: Score


class Basket(BaseModel):
    id_account: int | None = None
    shop: str | None = None
    name: str | None = None
    price: str | None = None
    description: str | None = None

