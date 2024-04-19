import asyncio
import logging
from data.config import dp, bot, client_s

from handlers import routers
from models.DatabaseModels import test
from models.db import global_init
from service import middleware

logger = logging.getLogger(__name__)


async def main() -> None:
    await global_init()
    await test()
    # await startTGClient(client_s=client_s)
    # for router in routers:
    #     dp.include_router(router)
    # dp.update.middleware(middleware.Logging())
    # await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-3s [%(asctime)s] - %(message)s',
        filemode="w",
        encoding='utf-8')

    with suppress(KeyboardInterrupt):
        asyncio.run(main())
