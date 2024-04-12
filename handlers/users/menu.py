from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from data.config import bot
from models.DatabaseModels import Users
from models.db import session_db
from service import keyboards as kb
from service.GetMessage import get_mes
from service.keyboards import Keyboards as kb

router = Router()


@router.callback_query(F.data == "back_menu")
@router.message(Command("start"))
@session_db
async def start(message: Message | CallbackQuery, session: AsyncSession):
    id = message.from_user.id
    is_reg = await Users.is_register(id, session)
    if is_reg is False:
        await Users.register(id=id, username=message.from_user.username, session=session)
    user = await Users.obj(id=id, session=session)

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


@router.callback_query(F.data == "shop")
async def shop_callback(message: CallbackQuery):
    id = message.from_user.id
    ...


menu_rt = router
