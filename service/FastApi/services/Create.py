import logging

import aiohttp

# from config.config import SECRET_KEY
from config.config import config
from internal.entities.database import accounts, categories, subcategories
from internal.entities.models import ApiPoint
from internal.entities.schemas.Catalog import Catalog
from internal.entities.schemas.Shop import Shop

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
            "auth_key": config.fastapi.private_key,
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


async def get_unique_instances_with_count() -> Catalog:
    """
    Получить список уникальных аккаунтов с view_type=True,
    сгруппированных по (shop, name), а также количество
    аккаунтов для каждой группы.
    """
    # Фильтр для выборки только активных аккаунтов
    instances = await accounts.get_view()
    # Словарь для группировки аккаунтов
    grouped_instances = {}
    for account in instances:
        subcategory = await subcategories.get(account.subcategory_id)
        category = await categories.get(subcategory.category_id)
        key = (category, subcategory, account.name)  # Уникальный ключ: (shop, name)
        if key not in grouped_instances:
            grouped_instances[key] = {
                "category": category.name,
                "subcategory": subcategory.name,
                "name": account.name,
                "description": account.description,
                "price": account.price,
                "uid": account.uid,
                "count": 0,
            }

        grouped_instances[key]["count"] += 1

    data = {"accounts": list(grouped_instances.values())}
    catalog = Catalog(**data)
    return catalog
