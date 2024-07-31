import logging
from typing import Any

from sqlalchemy import Column, String, Boolean, FLOAT, Integer

from .base import Base, BaseDB

logger = logging.getLogger(__name__)


class Account(Base):
    __tablename__ = "accounts"
    id: int = Column(Integer, autoincrement="auto", primary_key=True)
    shop: str = Column(String)
    price: float = Column(FLOAT)
    description: str = Column(String)
    data: str = Column(String)
    view_type: bool = Column(Boolean)
    name: str = Column(String)

    def dict(self):
        return {
            "id": self.id,
            "shop": self.shop,
            "price": self.price,
            "description": self.description,
            "data": self.data,
            "view_type": self.view_type,
            "name": self.name,
        }


class Accounts(BaseDB):
    async def new(self, account: Account):
        await self._add_obj(account)

    async def get(self, id: int) -> Account | None:
        result = await self._get_object(Account, id)
        return result

    async def update(self, account: Account) -> None:
        await self._update_obj(instance=account, obj=Account)

    async def delete(self, account: Account) -> None:
        await self._delete_obj(instance=account)

    async def in_(self, id: int) -> Account | bool:
        result = await self.get(id)
        if result is Account:
            return result
        return False

    async def get_shops(self) -> list[Any]:
        filters = {Account.view_type: True}
        data = await self._get_objects(obj=Account, filters=filters)
        result = []
        [result.append(i.shop) for i in data if i.shop not in result]
        return result

    async def get_account_by_name(self, name, shop):
        filters = {Account.name: name, Account.shop: shop, Account.view_type: True}
        result: list[Account] = await self._get_objects(obj=Account, filters=filters)
        account = result
        return account

    async def get_name_accounts_shop(self, shop: str):
        filters = {Account.shop: shop, Account.view_type: True}
        request = await self._get_objects(obj=Account, filters=filters)
        result = []
        for i in request:
            if len(i.name) < 65 and i.name not in result:
                result.append(i.name)
        logger.info(f"result: {result}")
        logger.info(f"request: {request}")


        filters = {Account.shop: shop}
        request = await self._get_objects(obj=Account, filters=filters)
        logger.info(f"request: {request}")
        return result
    
    async def get_last(self) -> Account:
        filters = {}
        data = await self._get_objects(Account, filters)
        return data[-1]
