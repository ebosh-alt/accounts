import logging

from data.config import BASE_PERCENT
from models.database import sellers, Seller, deals, Deal, accounts, Account
import time
import datetime
import asyncio

from models.database.base import create_async_database

logger = logging.getLogger(__name__)


async def checking_payment_status():
    await create_async_database()
    while True:
        unpaid_deals: list[Deal] = await deals.get_unpaid_deals()
        logger.info(f"unpaid_deals: {unpaid_deals}")
        for deal in unpaid_deals:
            if datetime.datetime.now() - deal.date >= datetime.timedelta(hours=1):
                account: Account = await accounts.get(id=deal.account_id)
                account.view_type = True
                await accounts.update(account=account)
                await deals.delete(deal=deal)
        guarantor_deals: list[Deal] = await deals.get_guarant_deals()
        for deal in guarantor_deals:
            if datetime.datetime.now() - deal.date >= datetime.timedelta(hours=24):
                seller: Seller = await sellers.get(id=deal.seller_id)
                account: Account = await accounts.get(id=deal.account_id)
                # seller.balance += float("%.2f" % (account.price * (1 - BASE_PERCENT / 100)))
                seller.balance += account.price
                await sellers.update(seller=seller)
                deal.payment_status = 2
                await deals.update(deal=deal)

        time.sleep(1 * 60)


def run_checker():
    asyncio.run(checking_payment_status())
