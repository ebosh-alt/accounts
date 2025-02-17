from datetime import datetime

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ForceReply

from data.config import bot
from filters.Filters import IsManager
from models.StateModels import Deal as Deal_
from models.database import sellers, Seller
from service.GetMessage import get_mes
from service.is_float import is_float
from service.keyboards import Keyboards
from states.states import ManagerStates

router = Router()


@router.callback_query(F.data == "change_wallet")
async def change_wallet_start(message: CallbackQuery, state: FSMContext):
    await state.set_state(ManagerStates.change_wallet)
    seller = await sellers.get(message.from_user.id)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("change_wallet_start", seller=seller),
        reply_markup=Keyboards.manager_back_menu_kb,
        parse_mode=ParseMode.MARKDOWN_V2
    )

@router.message(ManagerStates.change_wallet, IsManager())
async def change_wallet_1(message: Message, state: FSMContext):
    seller = await sellers.get(message.from_user.id)
    seller.wallet = message.text
    await sellers.update(seller)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("change_wallet_1", wallet=seller.wallet),
        reply_markup=Keyboards.manager_back_menu_kb,
        # parse_mode=ParseMode.MARKDOWN_V2
    )

wallet_rt = router