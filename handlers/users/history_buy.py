from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from data.config import bot
from models.database import users
from service.GetMessage import get_mes
from service.keyboards import Keyboards

router = Router()


@router.callback_query(F.data == "history_buy")
async def shop_callback(message: CallbackQuery):
    id = message.from_user.id
    data = await users.get_deals(id)
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("history_buy_user", deals=data),
                                reply_markup=Keyboards.back_menu_kb,
                                parse_mode=ParseMode.MARKDOWN_V2)


history_buy_rt = router
