import asyncio
import logging
from multiprocessing import Process

from aiogram.types import BotCommand

from config.config import config
from internal.handlers import routers
from internal.entities.database import sellers, Seller, shops, Shop, users, User
from internal.app.app import bot, dp
from internal.entities.database.base import create_async_database
from internal.entities.schemas.Shop import Shop as SchemaShop
from internal.handlers import routers
from service import middleware
from service.Background.checker import run_checker
from service.Excel.excel import Excel
from service.FastApi.events import create_fastapi, start_fastapi
from service.FastApi.services.Create import create_shop
from tests.test import create_test_data

import sys


logger = logging.getLogger(__name__)

async def run():
    await create_async_database()
    await init_main_data()
    shop = await shops.get(1)
    await create_shop(shop=SchemaShop(
        host=config.server.host,
        port=config.server.port,
        name=shop.name,
    ))

    app = create_fastapi()
    _ = asyncio.create_task(start_fastapi(app))

    bg_proc = Process(target=run_checker)
    bg_proc.start()
    if await sellers.in_(id=config.manager.seller_id):
        pass
    else:
        seller = Seller(id=config.manager.seller_id, rating=5, balance=0, username=config.manager.username, wallet="wallet")
        await sellers.new(seller=seller)
    for router in routers:
        dp.include_router(router)
    dp.update.middleware(middleware.Logging())
    await set_commands()

async def run_api():
    await create_async_database()
    await create_test_data()
    app = create_fastapi()
    await start_fastapi(app)

async def run_test():
    await create_async_database()
    await init_main_data()
    if len(sys.argv) > 1:
        if sys.argv[1] == "test_data":
            await create_test_data()
    # await categories.get(1)
    # await create_test_data()
    for router in routers:
        dp.include_router(router)
    dp.update.middleware(middleware.Logging())
    await set_commands()
    await dp.start_polling(bot)


async def set_commands():
    await bot.set_my_commands(commands=[
        BotCommand(command="start", description="перезапустить бота")
        # BotCommand(command="admin", description="АДМИН"),
        # BotCommand(command="manager", description="МЕНЕДЖЕР")
        ])
    
async def init_main_data():
    # Добавление записи в таблицу sellers
    if await sellers.in_(id=config.manager.seller_id):
        pass
    else:
        seller = Seller(id=config.manager.seller_id, rating=5, balance=0, username=config.manager.username, wallet="wallet")
        await sellers.new(seller=seller)

    # Добавление записей в таблицу users
    if await users.in_(id=config.manager.seller_id):
        pass
    else:
        user = User(id=config.manager.seller_id, username=config.manager.username)
        await users.new(user)

    # Добавление записи в таблицу shops
    shop = await shops.get(1)
    if shop is None:
        shop = Shop(
            name=config.shop.name,
            description=config.shop.description,
            path_photo=config.shop.path_photo,
        )
        await shops.new(shop)