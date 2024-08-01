import logging

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile

from data.config import bot
from models.database import users, User
from service.GetMessage import get_mes
from service.buy_automatically import clear_state_shopping_cart
from service.keyboards import Keyboards
from states.states import UserStates

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query((F.data == "back_menu") | (F.data == "В главное меню") | (F.data == "Вернуться в главное меню"))
@router.message(Command("start"))
async def start(message: Message | CallbackQuery, state: FSMContext):
    id = message.from_user.id
    if await state.get_state() == UserStates.ShoppingCart:
        await clear_state_shopping_cart(state, user_id=id)
    photo = FSInputFile("data/main.jpg")

    user = await users.in_(id=id)
    if user is False:
        user = User(id=id, username=message.from_user.username)
        await users.new(user)

    if type(message) is CallbackQuery:
        await message.message.delete()

    await bot.send_photo(chat_id=id,
                         photo=photo,
                         caption=get_mes("menu"),
                         reply_markup=Keyboards.menu_kb)


@router.callback_query(F.data == "rules")
async def rules_callback(message: CallbackQuery):
    id = message.from_user.id

    await message.message.delete()

    await bot.send_message(chat_id=id,
                           # message_id=message.message.message_id,
                           text=get_mes("rules"),
                           reply_markup=Keyboards.back_menu_kb,
                           parse_mode=ParseMode.MARKDOWN_V2)


@router.message(Command("chat_id"))
async def chat_id_e(message: Message | CallbackQuery):
    await bot.send_message(chat_id=message.chat.id,
                           text=str(message.chat.id))


menu_rt = router
