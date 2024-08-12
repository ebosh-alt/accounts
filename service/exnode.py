import asyncio
import json
from dataclasses import dataclass

import hmac
import hashlib
import time

import aiohttp
import requests

api_publi = "6ou06aogswjhwyzkyxy54ey7cny2olly24wxfh9u8ynffprzb7lv217odtt4yf0a"
api_privat = "ebho8jloorkzcrzgvqcs0p1ycakcmfr74erudcwhbgminzfxgl8jiy93szxdl6dadgdoam277eoxg3617si0mk49yes2r3874ha8ft0a650rwy2buoqk6okfn26z5wjp"


@dataclass
class ApiPoint:
    create_invoice = "https://my.exnode.ru/api/transaction/create/in"
    get_invoice = "https://my.exnode.ru/api/crypto/invoice/get?tracker_id={id}"
    token_fetch = "https://my.exnode.ru/user/token/fetch"


class ExNode:
    def __init__(self, api_public: str, api_private: str):
        self.api_public = api_public
        self.api_private = api_private

    def generate_signature(self, timestamp: str, body: str = ""):
        """
        Генерирует подпись с использованием HMAC-SHA512.
        :param timestamp:
        :param body: Сообщение в виде строки
        :return: Подпись в виде строки (hex-формат)
        """
        message = f"{timestamp}{body}"
        message_bytes = message.encode('utf-8')
        key_bytes = self.api_private.encode('utf-8')
        signature = hmac.new(key_bytes, message_bytes, hashlib.sha512)
        return signature.hexdigest()

    def headers(self, signature, timestamp):
        headers = {
            "Timestamp": timestamp,
            "ApiPublic": self.api_public,
            "Signature": signature,
            "Content-Type": "application/json",
            "Accept": "application/json"

        }
        return headers

    async def get_token_fetch(self):
        async with aiohttp.ClientSession() as session:
            signature = self.generate_signature(str(int(time.time())))
            response = await session.get(url=ApiPoint.token_fetch,
                                         headers=self.headers(signature, str(int(time.time()))))
            data = await response.json()
            await session.close()
        return data

    async def create_invoice(self, client_transaction_id: str):
        async with aiohttp.ClientSession() as session:
            body = {
                "token": "USDTTRC",
                "client_transaction_id": "84e4acb5-07dascascascf-4245-9137-7299d19a7950",
                "transaction_description": "Some description",
                "address_type": "STATIC",
                "call_back_url": "https://webhook.site/test_url_v2"
            }
            body = json.dumps(body, indent=2)
            timestamp = str(int(time.time()))
            signature = self.generate_signature(body=body, timestamp=timestamp)
            headers = self.headers(signature=signature, timestamp=timestamp)
            response = requests.post(url=ApiPoint.create_invoice, headers=headers, data=body)
            data = response.json()
            await session.close()
        return data


async def main():
    en = ExNode(api_publi, api_privat)
    # print(await en.get_token_fetch())
    print(await en.create_invoice(""))


if __name__ == '__main__':
    asyncio.run(main())
