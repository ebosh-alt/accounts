from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile, Document, ForceReply
from aiogram.enums import ParseMode
from data.config import bot
from filters.Filters import IsManager, IsManagerMessageValid
from service.GetMessage import get_mes
from service.keyboards import Keyboards
from states.states import ManagerStates
from data.config import EXCEL_TEMPLATE_PATH, EXCEL_LOAD_FILE_PATH
from service.ExcelS.s import create_accounts
from models.StateModels import Deal as Deal_
from models.database import chats, Chat
from datetime import datetime

router = Router()


@router.message(F.chat.id != F.from_user.id)#(IsManagerMessageValid())
async def send_text_to_user(message: Message, state: FSMContext):
    chat: Chat = await chats.get(id=message.chat.id)
    if chat is not None:
        if message.from_user.id == chat.seller_id:
            try:
                await bot.send_message(
                    chat_id=chat.user_id,
                    text=message.text
                )
            except Exception as er:
                print(er)
        else:
            # id отправителя не соответсвует id seller
            pass
    else:
        # chat не существует
        pass

communication_rt = router