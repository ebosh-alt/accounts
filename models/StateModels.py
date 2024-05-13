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
    account_id: int | None = None
    shop: str | None = None
    account_name: str | None = None
    price: float | None = None
    description: str | None = None
    guarantor: bool | None = None
    message_id: int | None = None
    deal_id: int | None = None
    uuid: str | None = None


class Deal(BaseModel):
    user_id: int = None
    shop: str = None
    price: int = None
    description: str = None
    data: str = None
    name: str = None
    guarant_type: bool = None