from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from data.config import bot
from filters.Filters import IsShop, IsNameAccount
from models.StateModels import Basket
from service.GetMessage import get_mes
from service.keyboards import Keyboards as kb
from models.database import accounts
from states.states import UserStates

router = Router()


@router.callback_query(F.data == "shop")
async def shop_callback(message: CallbackQuery):
    id = message.from_user.id
    keyboard = await kb.shops_kb()
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("shop_user"),
                                reply_markup=keyboard)


@router.callback_query(IsShop())
async def choice_shop(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    shop = message.data
    await state.set_state(UserStates.basket)
    await state.update_data(basket=Basket(shop=shop))
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text="Выберите аккаунт",
                                reply_markup=await kb.name_accounts_shop_kb(shop=shop))


@router.callback_query(IsNameAccount())
async def choice_name(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    name = message.data
    data = await state.get_data()
    basket: Basket = data["basket"]
    basket.name = name
    account = await accounts.get_account_by_name(name)
    basket.id_account = account.id
    basket.price = account.price
    basket.description = account.description
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("basket_user",
                                             shop=basket.shop,
                                             name=basket.name,
                                             price=basket.price,
                                             description=basket.description
                                             ),
                                parse_mode=ParseMode.MARKDOWN_V2)

shop_rt = router
