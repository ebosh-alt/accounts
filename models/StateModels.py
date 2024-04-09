from pydantic import BaseModel


class Score(BaseModel):
    score_id: int
    amount: float
    is_payment: bool


class Account(BaseModel):
    id_account: int
    guarantor: bool
    score: Score
