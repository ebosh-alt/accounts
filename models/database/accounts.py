import logging
from typing import Coroutine, Any

from sqlalchemy import Column, String, Boolean, FLOAT, Integer, Row

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
        result = await self._get_obj(Account, id)
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

    async def get_shop(self) -> Coroutine[Any, Any, list[Row]]:
        result = await self._get_attribute(obj=Account, attribute="shop")
        return result
