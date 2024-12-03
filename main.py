import asyncio
import datetime
import json
import logging
from contextlib import suppress
from multiprocessing import Process

from aiogram.types import BotCommand

from data.config import dp, bot, SELLER, USERNAME, ExNode, MERCHANT_ID, client_s
from handlers import routers
from models.database import sellers, Seller, users, User, deals, Deal, accounts, Account
from models.database.base import create_async_database
from service import middleware
from service.Background.checker import run_checker
from service.Excel.excel import get_account_data
from service.TGClient import startTGClient
from service.exnode import test

logger = logging.getLogger(__name__)


async def set_commands():
    await bot.set_my_commands(commands=[BotCommand(command="start", description="перезапустить бота")])


async def create_test_data():
    # Добавление записи в таблицу sellers
    if await sellers.in_(id=SELLER):
        pass
    else:
        seller = Seller(id=SELLER, rating=5, balance=0, username=USERNAME, wallet="wallet")
        await sellers.new(seller=seller)

    # Добавление записей в таблицу users
    if await users.in_(id=SELLER):
        pass
    else:
        user = User(id=SELLER, username=USERNAME)
        await users.new(user=user)

    # Добавление записей в таблицу accounts
    for i in range(1, 11):
        account = Account(
            shop=f"shop_{i}",
            price=100.0 + i,
            description=f"Description {i}",
            data=f"Data {i}",
            view_type=bool(i % 2),
            name=f"Account {i}",
            deal_id=i % 4 + 1
        )
        await accounts.new(account)

    # Добавление записей в таблицу deals
    for i in range(1, 5):
        deal = Deal(
            buyer_id=i,
            seller_id=SELLER,
            price=100.0 + i,
            wallet=f"wallet_{i}",
            date=datetime.datetime.now(),
            guarantor=bool(i % 2),
            payment_status=0
        )
        await deals.new(deal)

    # Добавление записей в таблицу chats
    ### Нет необходимости в тестовых значениях


async def main() -> None:
    await create_async_database()
    # await create_test_data()
    # bg_proc = Process(target=run_checker)
    # bg_proc.start()
    if await sellers.in_(id=SELLER):
        pass
    else:
        seller = Seller(id=SELLER, rating=5, balance=0, username=USERNAME, wallet="wallet")
        await sellers.new(seller=seller)
    # await startTGClient(client_s=client_s)
    for router in routers:
        dp.include_router(router)
    dp.update.middleware(middleware.Logging())
    await set_commands()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        # filename="log.logging",
        format=u'%(filename)s:%(lineno)d #%(levelname)-3s [%(asctime)s] - %(message)s',
        filemode="w",
        encoding='utf-8')

    with suppress(KeyboardInterrupt):
        # asyncio.run(main())
        account_data = get_account_data(r"D:\tg_bots\accounts\service\Excel\template_del.xlsx")
        print(account_data)
