from aiogram import Router, F
from aiogram.types import CallbackQuery

from models.database import users, deals
from service import SendDeals
from service.keyboards import Keyboards

router = Router()


@router.callback_query(F.data == "history_buy")
async def shop_callback(message: CallbackQuery):
    id = message.from_user.id
    user_deals = await deals.get_user_deals(id)
    await SendDeals.send(
        message=message,
        all_data_deals=user_deals,
        keyboard=Keyboards.menu_kb
    )

history_buy_rt = router
