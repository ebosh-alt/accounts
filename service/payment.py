from enum import Enum
from pydantic import BaseModel


class Responses(Enum):
    PAYMENT = "payment"
    PAYMENT_INFO = "payment/info"


class RequestCreatePayment(BaseModel):
    amount: str
    currency: str
    order_id: str
    network: str
    url_success: str
    url_callback: str
    is_payment_multiple: bool
    lifetime: int
    accuracy_payment_percent: int
    additional_data: str
    currencies: list


class ResponseCreatePayment(BaseModel):
    uuid: str
    order_id: str
    amount: str
    payment_amount: str
    payer_amount: str
    discount_percent: str
    discount: str
    payer_currency: str
    currency: str
    merchant_amount: str
    network: str
    address: str
    from_address: str
    txid: str
    payment_status: str
    url: str
    expired_at: str
    is_final: str
    additional_data: str
    created_at: str
    updated_at: str


class RequestGetPayment(BaseModel):
    uuid: str
    order_id: str


class CryptoMus:
    def __init__(self):
        self.api = "https://api.cryptomus.com/v1/"

    def create_payment(self, data: RequestCreatePayment):
        ...

    def get_payment(self, uuid: str):
        ...
