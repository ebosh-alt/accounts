import base64
import hashlib
import json
from typing import Any

from adaptix.load_error import LoadError
from aiohttp import ClientSession

from data.config import DEFAULT_HEADERS, DEFAULT_TIMEOUT, JsonDumps, ResponseType, API_BASE_URL
from models.CryptomusModels import Method
from service.Cryptomus.exceptions import CryptomusError


class AIOHTTPSession:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = ClientSession()
        self.headers = DEFAULT_HEADERS
        self.timeout = DEFAULT_TIMEOUT
        self.json_dumps: JsonDumps = json.dumps

    def check_response(
            self,
            method: Method[ResponseType],
            status_code: int,
            data: dict[str, Any]
    ) -> ResponseType:
        try:
            json_data = self.json_dumps(data)
        except Exception as e:
            raise CryptomusError(f"Error while parsing json: {e}")

        if status_code == 200:
            try:
                obj = method.build_response(json_data)
            except LoadError as e:
                raise CryptomusError(f"Error while building response: {e}")
            return obj

        raise CryptomusError(f"Error while request [{status_code}]: {json_data}")

    async def make_request(self, method: Method[ResponseType]) -> ResponseType:
        url = API_BASE_URL.format(method.api_method)
        data = method.to_str() or ""
        sign = hashlib.md5(
            base64.b64encode(data.encode('ascii')) + self.api_key.encode('ascii')
        ).hexdigest()

        self.headers["sign"] = sign
        async with self.session.request(
                method.http_method,
                url,
                headers=self.headers,
                data=method.to_str(),
                timeout=self.timeout
        ) as response:
            return self.check_response(method, response.status, await response.json())

    async def __call__(self, method: Method[ResponseType]) -> ResponseType:
        return await self.make_request(method)

    async def close(self) -> None:
        await self.session.close()
