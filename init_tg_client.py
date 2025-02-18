import asyncio
import logging

from internal.app.app import client_s
from service.TGClient import startTGClient


async def init():
    await startTGClient(client_s=client_s)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        # filename="log.logging",
        format=u'%(filename)s:%(lineno)d #%(levelname)-3s [%(asctime)s] - %(message)s',
        filemode="w",
        encoding='utf-8')
    asyncio.run(init())
