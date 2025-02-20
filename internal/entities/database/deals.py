from __future__ import annotations

import logging

from sqlalchemy import Column, Boolean, BigInteger, ForeignKey, Integer, Float, String, DateTime

from internal.entities.models import DataDeals
from .accounts import Accounts
from .subcategories import Subcategories
from .categories import Categories
from .base import Base, BaseDB

logger = logging.getLogger(__name__)


class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, autoincrement="auto", primary_key=True)
    buyer_id = Column(BigInteger, ForeignKey("users.id"))
    seller_id = Column(BigInteger, ForeignKey("sellers.id"))
    price = Column(Float)
    wallet = Column(String)
    date = Column(DateTime)
    guarantor = Column(Boolean)
    payment_status = Column(Integer)

    refs = []

    def dict(self):
        return {
            "id": self.id,
            "buyer_id": self.buyer_id,
            "seller_id": self.seller_id,
            "price": self.price,
            "wallet": self.wallet,
            "date": self.date,
            "guarantor": self.guarantor,
            "payment_status": self.payment_status,
        }


class Deals(BaseDB):
    def __init__(self):
        super().__init__(Deal)

    async def new(self, instance: Deal):
        await self._add_obj(instance)

    async def get(self, id: int) -> Deal | None:
        result = await self._get_object(id)
        return result

    async def update(self, instance: Deal) -> None:
        await self._update_obj(instance=instance)

    async def delete(self, instance: Deal) -> None:
        await self._delete_obj(instance=instance)


    async def get_data_deals(self) -> list[DataDeals]:
        result = list()
        async for deal in self:
            accs = await Accounts().get_by_deal_id(deal_id=deal.id)
            subcats = Subcategories()
            cats = Categories()
            for account in accs:
                sc = await subcats.get(account.subcategory_id)
                c = await cats.get(sc.category_id)
                result.append(DataDeals(
                    id=deal.id,
                    category=c.name,
                    subcategory=sc.name,
                    name=account.name,
                    price=account.price,
                    description=account.description,
                    data=account.data,
                    date=deal.date.strftime("%d.%m.%Y в %H:%M"),
                    guarantor=deal.guarantor,
                    payment=deal.payment_status
                ))
        return result

    async def get_user_deals(self, id: int) -> list[DataDeals]:
        filters = {Deal.buyer_id: id}
        deals = await self._get_objects(filters=filters)
        result = list()

        for deal in deals:
            accs = await Accounts().get_by_deal_id(deal_id=deal.id)
            subcats = Subcategories()
            cats = Categories()
            for account in accs:
            # print(account.dict())
                sc = await subcats.get(account.subcategory_id)
                c = await cats.get(sc.category_id)
                data_deals = DataDeals(
                    id=deal.id,
                    category=c.name,
                    subcategory=sc.name,
                    name=account.name,
                    price=float(account.price),
                    description=account.description,
                    data=account.data,
                    date=deal.date.strftime("%d.%m.%Y в %H:%M "),
                    guarantor=deal.guarantor,
                    payment=deal.payment_status
                )
            if data_deals not in result:
                result.append(data_deals)
        return result

    async def in_(self, id: int) -> Deal | bool:
        result = await self.get(id)
        if type(result) is Deal:
            return result
        return False

    async def get_last_deal(self, user_id) -> Deal:
        filters = {Deal.buyer_id: user_id}
        data = await self._get_objects(filters)
        return data[-1]

    async def get_unpaid_deals(self) -> list[Deal]:
        filters = {Deal.payment_status: 0}
        data = await self._get_objects(filters)
        return data

    async def get_guarantor_deals(self) -> list[Deal]:
        filters = {Deal.guarantor: True}
        data = await self._get_objects(filters)
        return data

    async def get_all(self):
        return await self._get_objects({})
