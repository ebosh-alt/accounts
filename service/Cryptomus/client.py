import asyncio
import logging
from typing import Any

from data.config import cryptomus_api_key, cryptomus_merchant_id
from models.CryptomusModels import PaymentInfoResponse, GetPaymentInfo, CreateInvoice
from service.Cryptomus.session import AIOHTTPSession

logger = logging.getLogger(__name__)


class CryptomusClient:
    def __init__(self, merchant_id: str, api_key: str,) -> None:
        _session = AIOHTTPSession(api_key)
        _session.headers["merchant"] = merchant_id
        self.session = _session

    @staticmethod
    def __get_func_params(params: dict[str, Any]) -> dict[str, Any]:
        if params.get("self"):
            del params["self"]
        return {
            k: v for k, v in params.items()
            if v is not None
        }

    async def get_payment_info(
            self, uuid: str, order_id: str | None = None
    ) -> PaymentInfoResponse:
        return await self.session(GetPaymentInfo(uuid, order_id))

    async def create_invoice(
            self,
            amount: int | float | str,
            currency: str,
            order_id: str,
            *,
            network: str | None = None,
            url_return: str | None = None,
            url_success: str | None = None,
            url_callback: str | None = None,
            is_payment_multiple: bool = True,
            lifetime: int = 3600,
            to_currency: str | None = None,
            subtract: int = 0,
            accuracy_payment_percent: int = 0,
            additional_data: str | None = None,
            currencies: list[str] | None = None,
            except_currencies: list[str] | None = None,
            course_source: str | None = None,
            from_referral_code: str | None = None,
            discount_percent: int | None = None,
            is_refresh: bool = False
    ) -> PaymentInfoResponse:
        if not isinstance(amount, str):
            amount = str(amount)

        return await self.session(CreateInvoice(**self.__get_func_params(locals())))

    async def close_session(self) -> None:
        await self.session.close()


async def main():
    cl = CryptomusClient(merchant_id=cryptomus_merchant_id, api_key=cryptomus_api_key)

    ses = await cl.create_invoice(amount=100, currency="USD", order_id="12345")
    await cl.close_session()


if __name__ == "__main__":
    asyncio.run(main())
