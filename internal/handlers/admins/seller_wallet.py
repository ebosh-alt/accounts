from datetime import datetime

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ForceReply

from internal.app.app import bot
from internal.filters.Filters import IsAdmin
from internal.entities.database import sellers, Seller
from service.GetMessage import get_mes
from service.is_float import is_float
from service.keyboards import Keyboards
from internal.entities.states.states import AdminStates

router = Router()


@router.callback_query(F.data == "change_seller_wallet")
async def change_seller_wallet_start(message: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.change_seller_wallet)
    seller = await sellers.get()
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("change_seller_wallet_start", seller=seller),
        reply_markup=Keyboards.admin_back_menu_kb,
        parse_mode=ParseMode.MARKDOWN_V2
    )

@router.message(AdminStates.change_seller_wallet, IsAdmin())
async def change_seller_wallet_1(message: Message, state: FSMContext):
    seller = await sellers.get()
    seller.wallet = message.text
    await sellers.update(seller)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("change_seller_wallet_1", screening=False, seller=seller),
        reply_markup=Keyboards.admin_back_menu_kb,
        # parse_mode=ParseMode.MARKDOWN_V2
    )

seller_wallet_rt = router