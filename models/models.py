from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel


class DataDeals(BaseModel):
    id: int
    shop: str
    name: str
    price: float | int
    description: str
    data: str
    date: str
    guarantor: bool
    payment: int

    def len(self):
        return len(str(self.id) + str(self.shop) + str(self.name) + str(self.price) + str(self.description) + str(
            self.data) + str(self.date) + str(self.guarantor) + str(self.payment))


class CreatedWallet(BaseModel):
    status: str
    tracker_id: str | None = None
    token_name: str | None = None
    refer: str | None = None
    alter_refer: str | None = None
    description: str | None
    dest_tag: str | None = None
    extra_info: dict | None = None


class ReceivedOrder(BaseModel):
    status: str = None
    description: str = None
    tracker_id: str | None = None
    amount: float | None = None
    payed_amount: float | None = None
    token: str | None = None
    client_transaction_id: str | None = None
    date_create: str | None = None
    date_expire: str | None = None
    amount_delta: float | None = None
    receiver: str | None = None
    hash: str | None = None
    dest_tag: str | None = None
    callback_url: str | None = None
    fiat_amount: float | None = None
    fiat_currency: str | None = None
    fiat_payed_amount: float | None = None
    fiat_underpayemnt_amount: float | None = None
    underpayemnt_amount: float | None = None
    merchant_uuid: str | None = None
    pay_form_url: str | None = None


class CreatedOrder(BaseModel):
    status: str = None
    description: str = None
    tracker_id: str | None = None
    amount: float | None = None
    dest_tag: str | None = None
    receiver: str | None = None
    date_expire: str | None = None


class CreatedMerchant(BaseModel):
    status: str
    description: str


class TransferredMerchantAccountBalance(BaseModel):
    status: str
    description: str | None


class Transaction(BaseModel):
    amount: float
    callback_url: str | None
    client_transaction_id: str
    date_create: str
    date_update: str
    dest_tag: str | None
    extra_info: dict | None
    hash: str
    receiver: str
    merchant_uuid: str
    status: str
    token: str
    token_major_name: str
    tracker_id: str
    transaction_commission: float
    transaction_description: str | None
    type: str
    amount_usd: float
    invoice_amount_usd: float
    course: float


class ReceivedTransaction(BaseModel):
    status: str
    description: str
    transaction: Transaction | None = None


@dataclass
class ApiPoint:
    create_wallet = "https://my.exnode.ru/api/transaction/create/in"
    # webhook_create_wallet = f"https://{IP_ADDRESS}/transaction_wallet"
    create_invoice = "https://my.exnode.ru/api/crypto/invoice/create"
    get_order = "https://my.exnode.ru/api/crypto/invoice/get"
    # webhook_get_order = f"https://{IP_ADDRESS}/get_order"
    token_fetch = "https://my.exnode.ru/user/token/fetch"
    create_order = "https://my.exnode.ru/api/crypto/invoice/create"
    # webhook_create_order = f"https://{IP_ADDRESS}/create_order"
    create_merchant = "https://my.exnode.ru/api/merchant/create"
    transfer_merchant_account_balance = "https://my.exnode.ru/api/merchant/transfer/all"
    create_withdrawal = "https://my.exnode.ru/api/transaction/create/out"
    # webhook_create_withdrawal = f"https://{IP_ADDRESS}/create_withdrawal"
    get_transaction = "https://my.exnode.ru/api/transaction/get"
    token_list = "https://my.exnode.ru/user/token/fetch"
    balance = "https://my.exnode.ru/api/token/balance"


class AccountExcel(BaseModel):
    type_account: str
    name: str
    price: Optional[float] = None
    description: Optional[str] = None
    data: Optional[str] = None
    uid: int
