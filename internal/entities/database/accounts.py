import logging
from typing import Any

from sqlalchemy import Column, String, Boolean, FLOAT, Integer, ForeignKey

# from internal.entities.database.categories import Categories
from internal.entities.database.subcategories import Subcategories
from internal.entities.schemas.Catalog import Catalog
from .base import Base, BaseDB


logger = logging.getLogger(__name__)


class Account(Base):
    __tablename__ = "accounts"

    id: int = Column(Integer, autoincrement=True, primary_key=True)
    subcategory_id: str = Column(Integer, ForeignKey("subcategories.id"))
    price: float = Column(FLOAT)
    description: str = Column(String)
    data: str = Column(String)
    view_type: bool = Column(Boolean)
    name: str = Column(String)
    deal_id: int = Column(Integer)
    uid: str = Column(String, unique=True)

    refs = []

    # @property
    # async def category(self):
    #     subcategory = await Subcategories().get(self.subcategory_id)
    #     category = await Categories().get(subcategory.category_id)
    #     return category.name

    # @property
    # async def subcategory(self):
    #     subcategory = await Subcategories().get(self.subcategory_id)
    #     return subcategory.name

    def dict(self):
        return {
            "id": self.id,
            "subcategory_id": self.subcategory_id,
            "price": self.price,
            "description": self.description,
            "data": self.data,
            "view_type": self.view_type,
            "name": self.name,
            "deal_id": self.deal_id,
            "uid": self.uid,
        }


class Accounts(BaseDB):
    def __init__(self):
        super().__init__(Account)

    async def new(self, instance: Account):
        await self._add_obj(instance)

    async def get(self, id: int) -> Account | None:
        result = await self._get_object(id)
        return result

    async def update(self, instance: Account) -> None:
        await self._update_obj(instance=instance)

    async def delete(self, instance: Account) -> None:
        await self._delete_obj(instance=instance)

    async def in_(self, id: int) -> Account | bool:
        result = await self.get(id)
        if result is Account:
            return result
        return False

    # async def get_shops(self) -> list[Any]:
    #     filters = {Account.view_type: True}
    #     data = await self._get_objects(filters=filters)
    #     result = []
    #     [result.append(i.shop) for i in data if i.shop not in result]
    #     return result

    # TODO: edit logic
    async def get_instance_by_name(self, name: str, subcategory_id: int):
        filters = {Account.name: name, Account.subcategory_id: subcategory_id, Account.view_type: True}
        result: list[Account] = await self._get_objects(filters=filters)
        instance = result
        return instance

    # async def get_name_instances_shop(self, category_id: int):
    #     filters = {Account.category_id: category_id, Account.view_type: True}
    #     request = await self._get_objects(filters=filters)
    #     result = []
    #     for i in request:
    #         if len(i.name) < 65 and i.name not in result:
    #             result.append(i.name)
    #     return result


    async def get_last(self) -> Account:
        filters = {}
        data = await self._get_objects(filters)
        return data[-1]

    async def get_by_deal_id(self, deal_id) -> list[Account]:
        filters = {Account.deal_id: deal_id}
        result = await self._get_objects(filters)
        return result

    async def in_uid(self, value) -> Account | bool:
        result = await self._in(Account.uid, [value])
        if len(result) == 0:
            return False
        return result[0]

    async def get_unique_instances_with_count(self) -> Catalog:
        """
        Получить список уникальных аккаунтов с view_type=True,
        сгруппированных по (shop, name), а также количество
        аккаунтов для каждой группы.
        """
        # Фильтр для выборки только активных аккаунтов
        filters = {Account.view_type: True}
        instances: list[Account] = await self._get_objects(filters=filters)

        # Словарь для группировки аккаунтов
        grouped_instances = {}
        for instance in instances:
            key = (await instance.category, await instance.subcategory, instance.name)  # Уникальный ключ: (shop, name)
            if key not in grouped_instances:
                grouped_instances[key] = {
                    "category": await instance.category,
                    "subcategory": await instance.subcategory,
                    "name": instance.name,
                    "description": instance.description,
                    "price": instance.price,
                    "uid": instance.uid,
                    "count": 0,
                }

            grouped_instances[key]["count"] += 1

        data = {"accounts": list(grouped_instances.values())}
        catalog = Catalog(**data)
        return catalog

    async def get_by_uid(self, uid) -> Account | bool:
        filters = {Account.uid: uid}
        result = await self._get_objects(filters)
        if len(result) == 0:
            return False
        return result[0]
