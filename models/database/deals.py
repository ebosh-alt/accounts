from __future__ import annotations

import datetime
import logging
from typing import List

from aiogram.fsm.context import FSMContext
from sqlalchemy import Column, Boolean, BigInteger, ForeignKey, INTEGER, DATETIME, Integer, Float, String, DateTime

from data.config import SELLER
from .accounts import Accounts

from .base import Base, BaseDB
from ..StateModels import ShoppingCart
from .accounts import Accounts
from ..models import DataDeals

logger = logging.getLogger(__name__)


class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, autoincrement="auto", primary_key=True)
    buyer_id = Column(BigInteger, ForeignKey("users.id"))
    seller_id = Column(BigInteger, ForeignKey("sellers.id"))
    # account_id = Column(BigInteger, ForeignKey("accounts.id"))
    price = Column(Float)
    wallet = Column(String)
    date = Column(DateTime)
    guarantor = Column(Boolean)
    payment_status = Column(Integer)

    # group_id = Column(BigInteger)

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
    async def new(self, deal: Deal):
        await self._add_obj(deal)

    async def get(self, id: int) -> Deal | None:
        result = await self._get_object(Deal, id)
        return result

    async def update(self, deal: Deal) -> None:
        await self._update_obj(instance=deal, obj=Deal)

    async def delete(self, deal: Deal) -> None:
        await self._delete_obj(instance=deal)


    async def get_data_deals(self) -> list[DataDeals]:
        all_deals: list[Deal] = await self._get_objects(Deal, {})
        result = list()
        for deal in all_deals:
            accs = await Accounts().get_by_deal_id(deal_id=deal.id)
            for account in accs:
                result.append(DataDeals(
                    id=deal.id,
                    shop=account.shop,
                    name=account.name,
                    price=account.price,
                    description=account.description,
                    data=account.data,
                    date=deal.date.strftime("%d.%m.%Y в %H:%M"),
                    guarantor=deal.guarantor,
                    payment=deal.payment_status
                ))
        return result

    # async def get_data_deals(self) -> list[DataDeals]:
    #     all_deals: list[Deal] = await self._get_objects(Deal, {})
    #     result = list()

    #     for deal in all_deals:
    #         account = await Accounts().get(deal.account_id)
    #         result.append(DataDeals(
    #             id=deal.id,
    #             shop=account.shop,
    #             name=account.name,
    #             price=account.price,
    #             description=account.description,
    #             data=account.data,
    #             date=deal.date.strftime("%d.%m.%Y в %H:%M"),
    #             guarantor=deal.guarantor,
    #             payment=deal.payment_status
    #         ))
    #     return result

    async def get_user_deals(self, id: int) -> list[DataDeals]:
        filters = {Deal.buyer_id: id}
        deals = await self._get_objects(Deal, filters=filters)
        result = list()

        for deal in deals:
            accs = await Accounts().get_by_deal_id(deal_id=deal.id)
            for account in accs:
            # print(account.dict())
                data_deals = DataDeals(
                    id=deal.id,
                    shop=account.shop,
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
        data = await self._get_objects(Deal, filters)
        return data[-1]

    async def get_unpaid_deals(self) -> list[Deal]:
        filters = {Deal.payment_status: 0}
        data = await self._get_objects(Deal, filters)
        return data

    async def get_guarant_deals(self) -> list[Deal]:
        filters = {Deal.guarantor: True}
        data = await self._get_objects(Deal, filters)
        return data

    # async def create_deal(self, state: FSMContext, user_id: int, message_id: int):
    #     accounts = Accounts()
    #     data = await state.get_data()
    #     shopping_cart: ShoppingCart = data["ShoppingCart"]
    #     account = await accounts.get(shopping_cart.account_id)
    #     account.view_type = False
    #     deal = Deal(
    #         buyer_id=user_id,
    #         seller_id=SELLER,
    #         account_id=shopping_cart.account_id,
    #         date=datetime.datetime.now(),
    #         guarantor=shopping_cart.guarantor,
    #         payment_status=0
    #     )

    #     await accounts.update(account)
    #     await self.new(deal)
    #     deal = await self.get_last_deal(user_id)
    #     shopping_cart.deals_id = deal.id
    #     shopping_cart.message_id = message_id
    #     await state.update_data(ShoppingCart=shopping_cart)

    async def get_all(self):
        return await self._get_objects(Deal, {})

    # async def get_new_group_id(self):
    #     all_deals = await self._get_objects(Deal, {})
    #     count_group = []
    #     for deal in all_deals:
    #         if deal.group_id not in count_group:
    #             count_group.append(deal.group_id)
    #     return len(count_group)
