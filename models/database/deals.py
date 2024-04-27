from __future__ import annotations

import datetime
import logging

from aiogram.fsm.context import FSMContext
from sqlalchemy import Column, Boolean, BigInteger, ForeignKey, INTEGER, DATETIME, Integer

from data.config import SELLER
from .accounts import Accounts

from .base import Base, BaseDB
from ..StateModels import ShoppingCart
from .accounts import Accounts
from .data_deals import DataDeals

logger = logging.getLogger(__name__)


class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, autoincrement="auto", primary_key=True)
    buyer_id = Column(BigInteger, ForeignKey("users.id"))
    seller_id = Column(BigInteger, ForeignKey("sellers.id"))
    account_id = Column(BigInteger, ForeignKey("accounts.id"))
    date = Column(DATETIME)
    guarantor = Column(Boolean)
    payment_status = Column(INTEGER)

    def dict(self):
        return {
            "id": self.id,
            "buyer_id": self.buyer_id,
            "seller_id": self.seller_id,
            "account_id": self.account_id,
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


    async def get_deals(self, *args) -> list[Deal]:
        ...


    async def get_data_deals(self) -> list[Deal]:
        all_deals: list[Deal] = await self._get_objects(Deal, {})
        result = list()

        for deal in all_deals:
            account = await Accounts().get(deal.account_id)
            result.append(DataDeals(
                id=deal.id,
                shop=account.shop,
                name=account.name,
                price=account.price,
                description=account.description,
                data=account.data,
                date=deal.date,
                guarantor=deal.guarantor
            ))
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

    async def create_deal(self, state: FSMContext, user_id: int, message_id: int):
        accounts = Accounts()
        data = await state.get_data()
        shopping_cart: ShoppingCart = data["ShoppingCart"]
        account = await accounts.get(shopping_cart.account_id)
        account.view_type = False
        deal = Deal(
            buyer_id=user_id,
            seller_id=SELLER,
            account_id=shopping_cart.account_id,
            date=datetime.datetime.now(),
            guarantor=shopping_cart.guarantor,
            payment_status=0
        )

        await accounts.update(account)
        await self.new(deal)
        deal = await self.get_last_deal(user_id)
        shopping_cart.deal_id = deal.id
        shopping_cart.message_id = message_id
        await state.update_data(ShoppingCart=shopping_cart)
