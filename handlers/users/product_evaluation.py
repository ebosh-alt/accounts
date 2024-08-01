import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from data.config import bot
from models.database import deals, accounts, sellers
from service.GetMessage import get_mes
from service.keyboards import Keyboards

logger = logging.getLogger(__name__)
router = Router()
product_evaluation_rt = router


@router.callback_query(F.data.contains("ok_account_"))
async def complete_payment(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    data = message.data.replace("ok_account_", "")
    deals_id = data.split(",")
    account_id = None
    for deal_id in deals_id:
        deal = await deals.get(int(deal_id))
        deal.payment_status = 2
        await deals.update(deal)
        if account_id is None:
            account_id = deal.account_id
    account = await accounts.get(account_id)
    seller = await sellers.get()
    seller.balance += account.price * len(deals_id)
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("mark_seller"),
                                reply_markup=Keyboards.mark_seller_kb)


@router.callback_query(F.data.in_(("0", "1", "2", "3", "4", "5")))
async def set_mark(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    mark = int(message.data)
    seller = await sellers.get()
    seller.rating += mark
    await sellers.update(seller)
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text="Спасибо за оценку!",
                                reply_markup=Keyboards.confirm_payment_kb)

    await state.clear()
