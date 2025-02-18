from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from internal.app.app import bot
from internal.entities.database import chats, Chat
import logging


router = Router()

logger = logging.getLogger(__name__)

@router.message(F.chat.id != F.from_user.id)
async def send_text_to_user(message: Message):
    chat: Chat = await chats.get(id=message.chat.id)
    if chat is not None:
        if message.from_user.id == chat.seller_id:
            try:
                await bot.send_message(
                    chat_id=chat.user_id,
                    text=message.text
                )
            except Exception as er:
                logger.info(er)
        else:
            # id отправителя не соответсвует id seller
            pass
    else:
        # chat не существует
        pass

communication_rt = router