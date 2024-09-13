import asyncio
import hashlib
import hmac
import json
import logging
import time

import aiohttp

from models.models import CreatedWallet, ApiPoint, CreatedOrder, TransferredMerchantAccountBalance, ReceivedOrder, \
    ReceivedTransaction, CreatedMerchant

logger = logging.getLogger(__name__)


class ExNodeClient:
    def __init__(self, api_public: str, api_private: str):
        self.__api_public = api_public
        self.__api_private = api_private

    def __generate_signature(self, timestamp: str, body: str):
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
            logger.info(await response.text())
            data = await response.json()
            await session.close()
        return data

    async def __send_get_request(self, body: dict, url: str):
        async with aiohttp.ClientSession() as session:
            timestamp = str(int(time.time()))
            signature = self.__generate_signature(timestamp=timestamp, body="")
            headers = {
                "Timestamp": timestamp,
                "ApiPublic": self.__api_public,
                "Signature": signature,
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            response = await session.get(url=url, headers=headers, params=body)
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
            # "call_back_url": ApiPoint.webhook_create_wallet,
        }
        data = await self.__send_post_request(body=body, url=ApiPoint.create_wallet)
        return CreatedWallet(**data)

    async def token_list(self):
        data = await self.__send_get_request(body={}, url=ApiPoint.token_list)
        return data

    async def create_order(self, client_transaction_id: str, amount: float, merchant_uuid: str,
                           token: str = "USDTTRC", payform: bool = False) -> CreatedOrder:
        body = {
            "token": token,
            "amount": amount,
            "fiat_currency": "USD",
            "client_transaction_id": client_transaction_id,
            "payment_delta": 1,
            "payform": payform,
            "merchant_uuid": merchant_uuid,
            # "call_back_url": ApiPoint.webhook_create_order
        }
        data = await self.__send_post_request(body=body, url=ApiPoint.create_order)
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
            # "call_back_url": ApiPoint.webhook_create_withdrawal,
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

    async def get_balance(self):
        data = await self.__send_post_request(body={}, url=ApiPoint.balance)
        return data

async def main():
    en = ExNodeClient("6ou06aogswjhwyzkyxy54ey7cny2olly24wxfh9u8ynffprzb7lv217odtt4yf0a",
                      "ebho8jloorkzcrzgvqcs0p1ycakcmfr74erudcwhbgminzfxgl8jiy93szxdl6dadgdoam277eoxg3617si0mk49yes2r3874ha8ft0a650rwy2buoqk6okfn26z5wjp")
    order = await en.create_order(client_transaction_id="trasmlmas,,l,l,lsasasess", amount="10.0",
                                  merchant_uuid="ac9db73e-2937-439d-a949-5326e31816ea")
    print(order)
    # wallet = await en.create_wallet(client_transaction_id="trsess")
    # print(await en.get_order(order.tracker_id))
    # print(await en.get_order(b))
    ...



if __name__ == '__main__':
    asyncio.run(main())
