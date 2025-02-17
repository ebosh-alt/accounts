import requests
from typing import Dict, List, Any


class CryptoCloudClient:
    def __init__(self, api_key: str, shop_id: str):
        self.api_key = api_key
        self.shop_id = shop_id
        self.base_url = "https://api.cryptocloud.plus/v2/"

    def _send_request(self, endpoint: str, method: str = "POST", payload: Dict[str, Any] = None) -> Dict[str, Any]:
        headers = {"Authorization": f"Token {self.api_key}"}
        url = self.base_url + endpoint
        response = requests.request(method, url, headers=headers, json=payload)
        return response.json()

    # def create_invoice(self, invoice_data: Dict[str, Any]) -> Dict[str, Any]:
    def create_invoice(self, amount: float) -> Dict[str, Any]:
        invoice_data = {
            "amount": amount,
            "shop_id": self.shop_id,
            "currency": "USD",
        }
        return self._send_request("invoice/create", payload=invoice_data)

    def cancel_invoice(self, uuid: str) -> Dict[str, Any]:
        data = {"uuid": uuid}
        return self._send_request("invoice/merchant/canceled", payload=data)

    def list_invoices(self, start_date: str, end_date: str, offset: int = 0, limit: int = 10) -> Dict[str, Any]:
        data = {"start": start_date, "end": end_date, "offset": offset, "limit": limit}
        return self._send_request("invoice/merchant/list", payload=data)

    def get_invoice_info(self, uuids: List[str]) -> Dict[str, Any]:
        data = {"uuids": uuids}
        return self._send_request("invoice/merchant/info", payload=data)

    def get_balance(self) -> Dict[str, Any]:
        return self._send_request("merchant/wallet/balance/all")

    def get_statistics(self, start_date: str, end_date: str) -> Dict[str, Any]:
        data = {"start": start_date, "end": end_date}
        return self._send_request("invoice/merchant/statistics", payload=data)
