import asyncio
from contextlib import suppress
import logging

from data.config import dp, bot
from handlers import routers
from service import middleware
from service.TGClient import startTGClient
from models.db import global_init
logger = logging.getLogger(__name__)


async def main() -> None:
    await global_init()
    # await startTGClient(client_s=client_s)
    for router in routers:
        dp.include_router(router)
    dp.update.middleware(middleware.Logging())
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-3s [%(asctime)s] - %(message)s',
        filemode="w",
        encoding='utf-8')

    with suppress(KeyboardInterrupt):
        asyncio.run(main())
