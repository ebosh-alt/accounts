import logging
import datetime
from typing import Tuple

from aiogram.fsm.context import FSMContext

from data.config import bot, SELLER, BASE_PERCENT, PERCENT_GUARANTOR
from models.StateModels import ShoppingCart
from models.database import accounts, deals, Account, Deal

logger = logging.getLogger(__name__)


async def set_data_shopping_cart(state: FSMContext, **kwargs) -> tuple[ShoppingCart, int] | ShoppingCart:
    # message: str = None, name: str = None, guarantor: str = None
    data = await state.get_data()
    message = kwargs.get('message')
    name = kwargs.get('name')
    guarantor = kwargs.get('guarantor')
    shopping_cart: ShoppingCart = data.get("ShoppingCart")
    if shopping_cart is None:
        shopping_cart = ShoppingCart(shop=message)
    if name is not None:
        shopping_cart.name = name
        account = await accounts.get_account_by_name(name, shopping_cart.shop)
        shopping_cart.price = account[0].price
        shopping_cart.description = account[0].description
        return shopping_cart, len(account)
    elif guarantor is not None:
        # account = await accounts.get(shopping_cart.accounts_id[0])
        shopping_cart.guarantor = True if guarantor == "yes_guarantor" else False
        if shopping_cart.guarantor:
            shopping_cart.price = float(
                "%.2f" % (shopping_cart.price * (1 + PERCENT_GUARANTOR / 100) * shopping_cart.count))
        else:
            shopping_cart.price = float("%.2f" % (shopping_cart.price * (1 + BASE_PERCENT / 100) * shopping_cart.count))
    elif message == "back_to_choice_account":
        shop = shopping_cart.shop
        shopping_cart = ShoppingCart(shop=shop)
    elif message:
        shopping_cart = ShoppingCart(shop=message)
    await state.update_data(ShoppingCart=shopping_cart)
    logger.info(f"Shopping Cart: {shopping_cart}")
    return shopping_cart


async def create_deal(user_id: int, message_id: int, state: FSMContext):
    data = await state.get_data()
    shopping_cart: ShoppingCart = data["ShoppingCart"]
    list_accounts: list[Account] = await accounts.get_account_by_name(shop=shopping_cart.shop, name=shopping_cart.name)
    list_accounts = list_accounts[0:shopping_cart.count]
    group_id = await deals.get_new_group_id()
    for account in list_accounts:
        account.view_type = False
        await accounts.update(account)
        await deals.new(deal=Deal(
            buyer_id=user_id,
            seller_id=SELLER,
            account_id=account.id,
            price=shopping_cart.price,
            date=datetime.datetime.now(),
            guarantor=shopping_cart.guarantor,
            payment_status=0,
            group_id=group_id
        )
        )
        deal = await deals.get_last_deal(user_id)
        shopping_cart.accounts_id.append(account.id)
        shopping_cart.deals_id.append(deal.id)
    shopping_cart.message_id = message_id
    await state.update_data(ShoppingCart=shopping_cart)


async def clear_state_shopping_cart(state: FSMContext, user_id: int):
    data = await state.get_data()
    shopping_cart: ShoppingCart = data.get("ShoppingCart")
    if shopping_cart is not None:
        for account_id in shopping_cart.accounts_id:
            account = await accounts.get(account_id)
            if account is not None:
                account.view_type = True
                await accounts.update(account)
            if shopping_cart.message_id is not None:
                await bot.delete_message(chat_id=user_id,
                                         message_id=shopping_cart.message_id)
        for deal_id in shopping_cart.deals_id:
            deal = await deals.get(deal_id)
            if deal.payment_status == 0:
                await deals.delete(deal)
        # if shopping_cart.deals_id is not None:
        #     deal = await deals.get(shopping_cart.deal_id)
        #     await deals.delete(deal)
        await state.clear()
