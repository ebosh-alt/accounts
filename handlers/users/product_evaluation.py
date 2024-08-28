import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from data.config import bot, SELLER, MAIN_ADMIN
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
    accs = None
    for deal_id in deals_id:
        deal = await deals.get(int(deal_id))
        deal.payment_status = 2
        await deals.update(deal)
        if account is None:
            accs = await accounts.get_by_deal_id(deal_id=deal.id)
    # account = await accounts.get(account_id)
    account = accs[0]
    seller = await sellers.get()
    seller.balance += account.price * len(accs)
    #TODO: метод отправки денег селлеру
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("mark_seller"),
                                reply_markup=Keyboards.mark_seller_kb)


@router.callback_query(F.data.contains("defect_account_"))
async def defect_account(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    data = message.data.replace("defect_account_", "")
    deals_id = data.split(",")
    accs = None
    deal = None
    for deal_id in deals_id:
        deal = await deals.get(int(deal_id))
        deal.payment_status = 2
        await deals.update(deal)
        if account is None:
            accs = await accounts.get_by_deal_id(deal_id=deal.id)
            account = accs[0]

    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("go_to_support"),
                                reply_markup=Keyboards.support_kb)
    
    await bot.edit_message_text(chat_id=SELLER,
                                message_id=message.message.message_id,
                                text=get_mes("notify_seller_defect_acc", deal=deal),
                                )
    
    await bot.edit_message_text(chat_id=MAIN_ADMIN,
                                message_id=message.message.message_id,
                                text=get_mes("notify_admin_defect_acc", deal=deal),
                                reply_markup=Keyboards.freeze_deal_kb(deal_id=deal.id))
    




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
