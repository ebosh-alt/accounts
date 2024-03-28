import asyncio
from contextlib import suppress
import logging

from data.config import dp, bot
from handlers import routers

logger = logging.getLogger(__name__)


async def main() -> None:
    for router in routers:
        dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
        filemode="w",
        encoding='utf-8')

    logger.info("Starting bot")
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
