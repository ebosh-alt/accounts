import asyncio
import hashlib
import hmac
import json
import time
from dataclasses import dataclass

import aiohttp
from pydantic import BaseModel

# from data.config import IP_ADDRESS
IP_ADDRESS = "0.0.0.0"
api_publi = "6ou06aogswjhwyzkyxy54ey7cny2olly24wxfh9u8ynffprzb7lv217odtt4yf0a"
api_privat = "ebho8jloorkzcrzgvqcs0p1ycakcmfr74erudcwhbgminzfxgl8jiy93szxdl6dadgdoam277eoxg3617si0mk49yes2r3874ha8ft0a650rwy2buoqk6okfn26z5wjp"
merchant_id = "366fa27a-0c48-4d9f-be3e-94bdb724f10e"


class CreatedWallet(BaseModel):
    status: str
    tracker_id: str = None
    token_name: str = None
    refer: str = None
    alter_refer: str = None
    description: str | None
    dest_tag: str | None = None
    extra_info: dict | None = None


class ReceivedOrder(BaseModel):
    status: str
    tracker_id: str
    amount: float | None
    payed_amount: float
    token: str
    client_transaction_id: str
    date_create: str
    date_expire: str
    amount_delta: float
    receiver: str
    hash: str | None
    dest_tag: str | None
    callback_url: str
    fiat_amount: float
    fiat_currency: str
    fiat_payed_amount: float
    fiat_underpayemnt_amount: float
    underpayemnt_amount: float
    merchant_uuid: str
    pay_form_url: str


class CreatedOrder(BaseModel):
    status: str = None
    description: str = None
    tracker_id: str = None
    amount: str | None = None
    dest_tag: str | None = None
    receiver: str = None
    date_expire: str = None


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
    transaction: Transaction


@dataclass
class ApiPoint:
    create_wallet = "https://my.exnode.ru/api/transaction/create/in"
    webhook_create_wallet = f"https://{IP_ADDRESS}/transaction_wallet"
    create_invoice = "https://my.exnode.ru/api/crypto/invoice/create"
    get_order = "https://my.exnode.ru/api/crypto/invoice/get"
    webhook_get_order = f"https://{IP_ADDRESS}/get_order"
    token_fetch = "https://my.exnode.ru/user/token/fetch"
    create_order = "https://my.exnode.ru/api/crypto/invoice/create"
    webhook_create_order = f"https://{IP_ADDRESS}/create_order"
    create_merchant = "https://my.exnode.ru/api/merchant/create"
    transfer_merchant_account_balance = "https://my.exnode.ru/api/merchant/transfer/all"
    create_withdrawal = "https://my.exnode.ru/api/transaction/create/out"
    webhook_create_withdrawal = f"https://{IP_ADDRESS}/create_withdrawal"
    get_transaction = "https://my.exnode.ru/api/transaction/get"


class ExNode:
    def __init__(self, api_public: str, api_private: str):
        self.__api_public = api_public
        self.__api_private = api_private

    def __generate_signature(self, timestamp: str, body: str = ""):
        message = f"{timestamp}{body}"
        message_bytes = message.encode('utf-8')
        key_bytes = self.__api_private.encode('utf-8')
        signature = hmac.new(key_bytes, message_bytes, hashlib.sha512)
        return signature.hexdigest()

    def __headers(self, body: dict = ""):
        body = json.dumps(body, indent=2)
        timestamp = str(int(time.time()))
        signature = self.__generate_signature(timestamp=timestamp, body=body)
        headers = {
            "Timestamp": timestamp,
            "ApiPublic": self.__api_public,
            "Signature": signature,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        return headers, body

    async def __send_post_request(self, body: dict, url: str):
        async with aiohttp.ClientSession() as session:
            headers, body = self.__headers(body)
            response = await session.post(url=url, headers=headers, data=body)
            data = await response.json()
            await session.close()
        return data

    async def __send_get_request(self, body: dict, url: str):
        async with aiohttp.ClientSession() as session:
            headers, body = self.__headers()
            response = await session.post(url=url, headers=headers, params=body)
            data = await response.json()
            await session.close()
        return data

    async def create_wallet(self, client_transaction_id: str, token: str = "USDTTRC",
                            transaction_description: str = "Some description",
                            address_type="SINGLE") -> CreatedWallet:
        body = {
            "token": token,
            "client_transaction_id": client_transaction_id,
            "transaction_description": transaction_description,
            "address_type": address_type,
            "call_back_url": ApiPoint.webhook_create_wallet,
        }
        data = await self.__send_post_request(body=body, url=ApiPoint.create_wallet)
        return CreatedWallet(**data)

    async def create_order(self, client_transaction_id: str, amount: float, merchant_uuid: str,
                           token: str = "USDTTRC") -> CreatedOrder:
        body = {
            "token": token,
            "amount": amount,
            "fiat_currency": "USD",
            "client_transaction_id": client_transaction_id,
            "payment_delta": 1,
            "payform": True,
            "merchant_uuid": merchant_uuid,
            "call_back_url": ApiPoint.webhook_create_order
        }
        data = await self.__send_post_request(body=body, url=ApiPoint.create_order)
        print(data)
        return CreatedOrder(**data)

    async def transfer_merchant_account_balance(self, merchant_uuid: str) -> TransferredMerchantAccountBalance:
        body = {
            "merchant_uuid": merchant_uuid
        }
        data = await self.__send_post_request(body=body, url=ApiPoint.transfer_merchant_account_balance)
        return TransferredMerchantAccountBalance(**data)

    async def create_withdrawal(self, client_transaction_id: str, merchant_uuid: str, amount: float, receiver: str,
                                token: str = "USDTTRC", transaction_description: str = "withdrawal",
                                dest_tag: str = "withdrawal") -> TransferredMerchantAccountBalance:
        body = {
            "token": token,
            "client_transaction_id": client_transaction_id,
            "merchant_uuid": merchant_uuid,
            "amount": amount,
            "receiver": receiver,
            "transaction_description": transaction_description,
            "call_back_url": ApiPoint.webhook_create_withdrawal,
            "dest_tag": dest_tag
        }
        data = await self.__send_post_request(body=body, url=ApiPoint.create_withdrawal)
        return TransferredMerchantAccountBalance(**data)

    async def get_order(self, tracker_id: str) -> ReceivedOrder:
        body = {
            "tracker_id": tracker_id
        }
        data = await self.__send_get_request(body=body, url=ApiPoint.get_order)
        return ReceivedOrder(**data)

    async def get_transaction(self, tracker_id: str) -> ReceivedTransaction:
        body = {
            "tracker_id": tracker_id
        }
        data = await self.__send_post_request(body=body, url=ApiPoint.create_withdrawal)
        return ReceivedTransaction(**data)

    async def create_merchant(self, name: str, active_in: bool = True, active_out: bool = True) -> CreatedMerchant:
        body = {
            "name": name,
            "active_in": active_in,
            "active_out": active_out
        }
        data = await self.__send_post_request(body=body, url=ApiPoint.create_merchant)
        return CreatedMerchant(**data)


async def main():
    en = ExNode(api_publi, api_privat)
    # wallet = await en.create_wallet(client_transaction_id="tres")
    # print(wallet)
    order = await en.create_order(client_transaction_id="trses", amount=10.0,
                                  merchant_uuid="ac9db73e-2937-439d-a949-5326e31816ea")
    print(order)
    # get_order = await en.get_order(tracker_id=order.tracker_id)
    # print(get_order)


if __name__ == '__main__':
    asyncio.run(main())
