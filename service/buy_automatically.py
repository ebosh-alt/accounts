import logging

from aiogram.fsm.context import FSMContext

from data.config import PERCENT, bot
from models.StateModels import ShoppingCart
from models.database import accounts, deals

logger = logging.getLogger(__name__)


async def set_data_shopping_cart(state: FSMContext, **kwargs) -> ShoppingCart:
    # message: str = None, name: str = None, guarantor: str = None
    data = await state.get_data()
    message = kwargs.get('message')
    name = kwargs.get('name')
    guarantor = kwargs.get('guarantor')
    shopping_cart: ShoppingCart = data.get("ShoppingCart")
    if shopping_cart is None:
        shopping_cart = ShoppingCart(shop=message)
    if name is not None:
        shopping_cart.account_name = name
        account = await accounts.get_account_by_name(name)
        shopping_cart.account_id = account.id
        shopping_cart.price = account.price
        shopping_cart.description = account.description
    elif guarantor is not None:
        shopping_cart.guarantor = True if guarantor == "yes_guarantor" else False
        if shopping_cart.guarantor:
            shopping_cart.price = float("%.2f" % (shopping_cart.price * (1 + PERCENT / 100)))
    elif message == "back_to_choice_account":
        shop = shopping_cart.shop
        shopping_cart = ShoppingCart(shop=shop)
    elif message:
        shopping_cart = ShoppingCart(shop=message)
    await state.update_data(ShoppingCart=shopping_cart)
    logger.info(f"Shopping Cart: {shopping_cart}")
    return shopping_cart


async def clear_state_shopping_cart(state: FSMContext, user_id: int):
    data = await state.get_data()
    shopping_cart: ShoppingCart = data["ShoppingCart"]
    account = await accounts.get(shopping_cart.account_id)
    deal = await deals.get(shopping_cart.deal_id)
    account.view_type = True
    await bot.delete_message(chat_id=user_id,
                             message_id=shopping_cart.message_id)
    await accounts.update(account)
    await deals.delete(deal)
    await state.clear()
