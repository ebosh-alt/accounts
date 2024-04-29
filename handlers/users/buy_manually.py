import logging

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from data.config import bot, PERCENT, client_s, SELLER, BOT_ID
from filters.Filters import IsShop, IsNameAccount, IsUserMessageValid
from models.StateModels import ShoppingCart
from models.database import deals, accounts, sellers, chats, Chat
from service.GetMessage import get_mes
from service.keyboards import Keyboards
from states.states import UserStates


logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data == "Общение с продавцом")
async def start_mailing_to_seller(message: CallbackQuery, state: FSMContext):
    user_id = message.from_user.id
    await state.set_state(UserStates.MailingSeller)
    #Создание чата
    chat = await chats.get_chat_by_user(user_id=user_id)
    print("___________________",chat, "________________")
    if chat is None:
        chat_id, er = await client_s.createChat([SELLER, int(BOT_ID)], title=str(user_id))
        print(chat_id, er)
    else:
        chat_id = chat.id
        er = True
    if not er:
        chat = Chat(
            id=-chat_id,
            user_id=user_id,
            seller_id=SELLER,
        )
        await chats.new(chat=chat)
    await bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=message.message.message_id,
        text=get_mes("start_mailing_seller")
    )
    # print(chat_id)
    # await bot.send_message(
    #     chat_id=-chat_id,
    #     text="Ура!"
    # )


@router.message(UserStates.MailingSeller, IsUserMessageValid())
async def send_message_seller(message: Message, state: FSMContext):
    chat = await chats.get_chat_by_user(user_id=message.from_user.id)
    if chat is not None:
        await bot.send_message(
            chat_id=chat.id,
            text=message.text,
        )
    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_mes("err_send_text_manager"),
        )


buy_manually_rt = router
