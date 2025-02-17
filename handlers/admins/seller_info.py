from aiogram import Router, F
from aiogram.types import CallbackQuery

from data.config import bot
from filters.Filters import IsAdmin
from models.database import sellers
from service.GetMessage import get_mes
from service.keyboards import Keyboards

router = Router()


@router.callback_query(F.data == "show_seller_info", IsAdmin())
async def show_seller_info(message: CallbackQuery):
    try:
        seller = await sellers.get()
        await bot.edit_message_text(
            chat_id=message.message.chat.id,
            message_id=message.message.message_id,
            text=get_mes(
                "seller_info",
                user_id=seller.id,
                balance=seller.balance,
                rating=seller.rating,
                username=seller.username,
                wallet=seller.wallet
            ),
            reply_markup=Keyboards.admin_back_menu_kb
        )
    except Exception as er:
        await bot.send_message(
            chat_id=message.message.chat.id,
            text=get_mes("seller_info_er", er=er),
            reply_markup=Keyboards.admin_back_menu_kb
        )


seller_info_rt = router
