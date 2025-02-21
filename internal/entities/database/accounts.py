import logging

from sqlalchemy import Column, String, Boolean, FLOAT, Integer, ForeignKey

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


    # TODO: edit logic
    async def get_instance_by_name(self, name: str, subcategory_id: int):
        filters = {Account.name: name, Account.subcategory_id: subcategory_id, Account.view_type: True}
        result: list[Account] = await self._get_objects(filters=filters)
        instance = result
        return instance


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

    async def get_by_uid(self, uid) -> Account | bool:
        filters = {Account.uid: uid}
        result = await self._get_objects(filters)
        if len(result) == 0:
            return False
        return result[0]

    async def get_view(self):
        filters = {Account.view_type: True}
        instances: list[Account] = await self._get_objects(filters=filters)
        return instances