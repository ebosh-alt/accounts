import logging
from datetime import datetime

from sqlalchemy import Column, String, BigInteger

from . import Deal
from .accounts import Accounts

from .base import Base, BaseDB

from .data_deals import DataDeals

logger = logging.getLogger(__name__)

class DataDeals(BaseModel):
    id: int
    shop: str
    name: str
    price: float
    description: str
    data: str
    date: str
    guarantor: bool


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    username = Column(String)

    def dict(self):
        return {"id": self.id,
                "username": self.username,
                }


class Users(BaseDB):
    async def new(self, user: User):
        await self._add_obj(user)

    async def get(self, id: int) -> User | None:
        result = await self._get_object(User, id)
        return result

    async def get_data_deals(self, id: int) -> list[DataDeals]:
        filters = {Deal.buyer_id: id}
        deals = await self._get_objects(Deal, filters=filters)
        result = list()

        for deal in deals:
            account = await Accounts().get(deal.account_id)
            result.append(DataDeals(
                id=deal.id,
                shop=account.shop,
                name=account.name,
                price=account.price,
                description=account.description,
                data=account.data,
                date=deal.date.strftime("%d.%m.%Y в %H:%M "),
                guarantor=deal.guarantor
            ))
        return result

    async def update(self, user: User) -> None:
        await self._update_obj(instance=user, obj=User)

    async def delete(self, user: User) -> None:
        await self._delete_obj(instance=user)

    async def in_(self, id: int) -> User | bool:
        result = await self.get(id)
        if type(result) is User:
            return result
        return False
