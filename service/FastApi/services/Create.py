import logging

import aiohttp

from data.config import SECRET_KEY
from models.models import ApiPoint
from models.schemas.Shop import Shop

logger = logging.getLogger(__name__)


async def post(url: str, headers, data):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        response = await session.post(url=url, json=data, headers=headers)
        if response.status == 200:
            logger.info(f"Successfully response {url}, status: {response.status}")
        else:
            logger.info(f"Error response {url}, status: {response.status}")
        data = await response.json()
        await session.close()
    return data


async def create_shop(shop: Shop):
    try:
        headers = {
            "accept": "application/json",
            "auth_key": SECRET_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "name": shop.name,
            "host": shop.host,
            "port": shop.port,
        }
        data = await post(ApiPoint.get_shop, headers, data)
        logger.info(data)
    except Exception as e:
        logger.error(f"Error send request to create chop: \n{e}")
