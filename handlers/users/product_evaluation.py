import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from data.config import bot, SELLER, MAIN_ADMIN,  MERCHANT_ID
from service.exnode import ExNode

from models.database import deals, accounts, sellers
from models.models import TransferredMerchantAccountBalance
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
        if accs is None:
            accs = await accounts.get_by_deal_id(deal_id=deal.id)
    account = accs[0]
    seller = await sellers.get()
    seller.balance += account.price * len(accs)
    transfer: TransferredMerchantAccountBalance = await ExNode.create_withdrawal(
        client_transaction_id=deals_id[0],
        merchant_uuid=MERCHANT_ID,
        amount=account.price * len(accs),
        receiver=seller.wallet
    )
    if transfer.status == "ACCEPTED":
        await bot.send_message(chat_id=seller.id,
                               text="Выплата успешно завершена")
    else:
        await bot.send_message(chat_id=seller.id,
                               text="Произошла ошибка при выплате")
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("mark_seller"),
                                reply_markup=Keyboards.mark_seller_kb)
    await sellers.update(seller)


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
        if accs is None:
            accs = await accounts.get_by_deal_id(deal_id=deal.id)

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
                                reply_markup=Keyboards.confirm_payment_kb,
                                parse_mode=None)

    await state.clear()
