from pydantic import BaseModel


class Score(BaseModel):
    user_id: int | None
    amount: float
    guarantor: bool
    is_payment: bool


class Account(BaseModel):
    id_account: int
    score: Score
