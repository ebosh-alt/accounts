from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, User, CallbackQuery
from data.config import ADMINS
from models.database import accounts


class IsAdmin(Filter):
    async def __call__(self, message: Message, event_from_user: User) -> bool:
        if event_from_user.id in ADMINS:
            return True
        return False


class IsShop(Filter):
    async def __call__(self, message: CallbackQuery, event_from_user: User) -> bool:
        buttons = await accounts.get_shops()
        buttons.append("back_to_choice_account")
        if message.data in buttons:
            return True
        return False


class IsNameAccount(Filter):
    async def __call__(self, message: CallbackQuery, event_from_user: User, state: FSMContext) -> bool:
        data = await state.get_data()
        shopping_cart = data.get('ShoppingCart')
        buttons = await accounts.get_name_accounts_shop(shopping_cart.shop)
        if message.data in buttons:
            return True
        return False
