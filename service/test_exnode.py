import json

import requests
import hmac
import hashlib
import time
import http.client

api_private = "ebho8jloorkzcrzgvqcs0p1ycakcmfr74erudcwhbgminzfxgl8jiy93szxdl6dadgdoam277eoxg3617si0mk49yes2r3874ha8ft0a650rwy2buoqk6okfn26z5wjp"


def generate_signature(timestamp: str, body: str = ""):
    """
    Генерирует подпись с использованием HMAC-SHA512.
    :param timestamp:
    :param body: Сообщение в виде строки
    :return: Подпись в виде строки (hex-формат)
    """
    message = f"{timestamp}{body}"
    message_bytes = message.encode('utf-8')
    key_bytes = api_private.encode('utf-8')
    signature = hmac.new(key_bytes, message_bytes, hashlib.sha512)
    return signature.hexdigest()


def conn():
    conn = http.client.HTTPSConnection("my.exnode.ru")

    payload = "{\n  \"token\": \"USDTTRC\",\n  \"client_transaction_id\": \"84e4acb5-07df-4245-9137-7299d1s9as7950\",\n  \"transaction_description\": \"Some description\",\n  \"address_type\": \"STATIC\",\n  \"call_back_url\": \"https://webhook.site/test_url_v2\"\n}"

    ts = str(int(time.time()))
    headers = {
        'Timestamp': ts,
        'ApiPublic': "6ou06aogswjhwyzkyxy54ey7cny2olly24wxfh9u8ynffprzb7lv217odtt4yf0a",
        'Signature': generate_signature(ts, payload),
        'Content-Type': "application/json",
        'Accept': "application/json"
    }

    conn.request("POST", "/api/transaction/create/in", body=payload, headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))


def req():
    url = "https://my.exnode.ru/api/transaction/create/in"
    ts = str(int(time.time()))
    payload = "{\n  \"token\": \"USDTTRC\",\n  \"client_transaction_id\": \"84e4acb5-07lsdf-4245ascsa-9137-7299d1s9as7950\",\n  \"transaction_description\": \"Some description\",\n  \"address_type\": \"STATIC\",\n  \"call_back_url\": \"https://webhook.site/test_url_v2\"\n}"

    body = {
        "token": "USDTTRC",
        "client_transaction_id": "84e4acb5-07dfasasa-4245-9137-7299d19a7950",
        "transaction_description": "Some description",
        "address_type": "STATIC",
        "call_back_url": "https://webhook.site/test_url_v2"
    }
    body = json.dumps(body, indent=2)
    headers = {
        "Timestamp": ts,
        "ApiPublic": "6ou06aogswjhwyzkyxy54ey7cny2olly24wxfh9u8ynffprzb7lv217odtt4yf0a",
        "Signature": generate_signature(ts, body),
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post(url, data=body, headers=headers)

    print(response.json())


if __name__ == "__main__":
    req()
