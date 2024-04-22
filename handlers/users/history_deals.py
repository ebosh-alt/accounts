from aiogram import Router, F
from aiogram.types import CallbackQuery

from data.config import bot
from models.database import deals, users
from service.GetMessage import get_mes

router = Router()


@router.callback_query(F.data == "history_buy")
async def shop_callback(message: CallbackQuery):
    id = message.from_user.id
    data = await users.get_deals(id)
    await bot.send_message(chat_id=id, text=get_mes("history_buy_user", deals=data))


history_deals_rt = router
