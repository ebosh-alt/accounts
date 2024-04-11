from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Generic, cast, Any
from data.config import ResponseType, retort


class Method(Generic[ResponseType]):
    returning: json
    api_method: str
    http_method: str

    def to_str(self) -> str | None:
        return json.dumps(self.to_json())

    def to_json(self) -> dict[str, Any] | None:
        return cast(dict[str, Any], retort.dump(self))

    def build_response(self, json_string: str) -> ResponseType:
        return self.returning.from_json(json.loads(json_string))


@dataclass
class PaymentInfoResponse:
    state: int
    uuid: str
    order_id: str
    amount: float
    payment_status: str
    url: str
    expired_at: int
    status: str
    is_final: bool
    created_at: datetime
    updated_at: datetime
    commission: float
    payment_amount: float | None = None
    payment_amount_usd: float | None = None
    payer_amount: float | None = None
    additional_data: str | None = None
    payer_amount_exchange_rate: float | None = None
    discount_percent: float | None = None
    discount: float | None = None
    payer_currency: str | None = None
    currency: str | None = None
    comments: str | None = None
    merchant_amount: float | None = None
    network: str | None = None
    address: str | None = None
    from_: str | None = None
    txid: str | None = None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> PaymentInfoResponse:
        from_ = data["result"].pop("from", None)
        return cls(state=data["state"], from_=from_, **data["result"])


@dataclass
class MoneyAmount:
    amount: float
    payment_amount: float
    payment_amount_usd: float
    payer_amount: float
    payer_amount_exchange_rate: float | None
    discount_percent: float
    discount: float
    payer_currency: str


@dataclass
class GetPaymentInfo(Method[PaymentInfoResponse]):
    __returning__ = PaymentInfoResponse
    __api_method__ = "v1/payment/info"
    __http_method__ = "post"

    uuid: str
    order_id: str | None = None


@dataclass
class CreateInvoice(Method[PaymentInfoResponse]):
    returning = PaymentInfoResponse
    api_method = "v1/payment"
    http_method = "post"

    amount: int | float | str
    currency: str
    order_id: str
    lifetime: int
    network: str | None = None
    url_return: str | None = None
    url_success: str | None = None
    url_callback: str | None = None
    is_payment_multiple: bool = True
    to_currency: str | None = None
    subtract: int = 0
    accuracy_payment_percent: int = 0
    additional_data: str | None = None
    currencies: list[str] | None = None
    except_currencies: list[str] | None = None
    course_source: str | None = None
    from_referral_code: str | None = None
    discount_percent: int | None = None
    is_refresh: bool = False
