from multiprocessing import Process
from models.database import sellers, Seller, deals, Deal, accounts, Account
import time
import datetime
import asyncio


async def checking_payment_status():
    while True:
        # print("Смотрю")
        unpaid_deals: list[Deal] = await deals.get_unpaid_deals()
        for deal in unpaid_deals:
            # print(deal.date)
            # print(deal.date,",", datetime.datetime.now(),",", deal.date - datetime.datetime.now(),",", datetime.timedelta(minutes=1))
            if datetime.datetime.now() - deal.date >= datetime.timedelta(hours=1):
                account: Account = await accounts.get(id=deal.account_id)
                account.view_type = True
                await accounts.update(account=account)
                await deals.delete(deal=deal)
        guarant_deals: list[Deal] = await deals. get_guarant_deals()
        for deal in guarant_deals:
            if datetime.datetime.now() - deal.date >= datetime.timedelta(hours=24):
                seller: Seller = await sellers.get(id=deal.seller_id)
                account: Account = await accounts.get(id=deal.account_id)
                seller.balance += account.price
                await sellers.update(seller=seller)
                deal.payment_status=2
                await deals.update(deal=deal)

        time.sleep(1*60)

def run_checker():
    asyncio.run(checking_payment_status())