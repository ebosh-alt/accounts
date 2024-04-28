from pydantic import BaseModel


class Score(BaseModel):
    user_id: int | None
    amount: float
    guarantor: bool
    is_payment: bool


class Account(BaseModel):
    id_account: int
    score: Score

class Deal(BaseModel):
    user_id: int = None
    shop: str = None
    price: int = None
    description: str = None
    data: str = None
    name: str = None
    guarant_type: bool = None