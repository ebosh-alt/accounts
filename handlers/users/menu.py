from datetime import datetime
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from models.database import accounts, deals, Deal, Account, sellers, Seller, users, User
from data.config import bot
from service import keyboards as kb
from service.GetMessage import get_mes
from service.keyboards import Keyboards as kb

router = Router()


# @router.message(Command("test"))
# async def test(message: Message | CallbackQuery):
#     user = await users.get(id=message.from_user.id)
#     print(user.dict())


@router.callback_query(F.data == "back_menu")
@router.message(Command("start"))
async def start(message: Message | CallbackQuery):
    id = message.from_user.id
    user = await users.in_(id=id)
    if user is False:
        user = User(id=id, username=message.from_user.username)
        await users.new(user)

    if type(message) is Message:
        await bot.send_message(chat_id=id,
                               text=get_mes("menu"),
                               reply_markup=kb.menu_kb)
    else:
        await bot.edit_message_text(chat_id=id,
                                    message_id=message.message.message_id,
                                    text=get_mes("menu"),
                                    reply_markup=kb.menu_kb)


@router.callback_query(F.data == "rules")
async def rules_callback(message: CallbackQuery):
    id = message.from_user.id
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("rules"),
                                reply_markup=kb.back_menu_kb)


@router.callback_query(F.data == "history_buy")
async def history_buy_callback(message: CallbackQuery):
    id = message.from_user.id
    ...

menu_rt = router
