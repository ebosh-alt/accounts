import asyncio
import logging
from contextlib import suppress

from aiogram.types import BotCommand

from data.config import dp, bot, client_s, SELLER, USERNAME

from handlers import routers
from models.database.base import create_async_database
from service import middleware
from tests.test import new_data
from service.TGClient import startTGClient
from models.database import sellers, Seller
from multiprocessing import Process
from service.Background.checker import run_checker

logger = logging.getLogger(__name__)


async def set_commands():
    await bot.set_my_commands(commands=[BotCommand(command="start", description="перезапустить бота")])


async def main() -> None:
    await create_async_database()
    # bg_proc = Process(target=run_checker)
    # bg_proc.start()
    if await sellers.in_(id=SELLER):
        pass
    else:
        seller = Seller(id=SELLER, rating=5, balance=0, username=USERNAME)
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
        asyncio.run(main())
