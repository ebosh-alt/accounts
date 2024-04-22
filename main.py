import asyncio
import logging
from data.config import dp, bot, client_s

from handlers import routers
from models.database.base import create_async_database
# from models.database.deals import test
from models.database.users import test_user
from service import middleware
from tests.test import new_data

logger = logging.getLogger(__name__)


async def main() -> None:
    await create_async_database()
    await test_user()
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
