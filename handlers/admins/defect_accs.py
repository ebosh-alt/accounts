from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from data.config import bot, SELLER, MAIN_ADMIN
from filters.Filters import IsAdmin
from service.GetMessage import get_mes
from service.keyboards import Keyboards
from models.database import deals, sellers, accounts
from models.StateModels import Deal as Deal_
from states.states import AdminStates


router = Router()


@router.callback_query(F.data.contains("admin_freeze_deal_"), IsAdmin())
async def admin_freeze_deal(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    deal_id = int(message.data.replace("admin_freeze_deal_", ""))
    deal = await deals.get(id=deal_id)
    await bot.send_message(chat_id=deal.buyer_id,
                                text=get_mes("notify_buyer_freezed_deal"),
                                reply_markup=Keyboards.support_kb)
    
    await bot.send_message(chat_id=SELLER,
                                text=get_mes("notify_seller_freezed_deal", deal=deal),
                                )
    
    await bot.edit_message_text(chat_id=MAIN_ADMIN,
                                message_id=message.message.message_id,
                                text=get_mes("descision_on_deal", deal=deal),
                                reply_markup=Keyboards.descision_deal_freezing(deal_id=deal.id))


@router.callback_query(F.data.contains("confirm_freezed_deal_"), IsAdmin())
async def confirm_freezed_deal(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    deal_id = int(message.data.replace("confirm_freezed_deal_", ""))
    deal = await deals.get(id=deal_id)
    seller = await sellers.get()
    seller.balance += deal.price
    deal.payment_status = 2
    await sellers.update(seller=seller)
    await deals.update(deal=deal)
    await bot.send_message(chat_id=deal.buyer_id,
                                text=get_mes("notify_buyer_confirmation_deal", deal=deal),
                                reply_markup=Keyboards.support_kb)
    
    await bot.send_message(chat_id=SELLER,
                                text=get_mes("notify_seller_confirmation_deal", deal=deal),
                                )
    
    await bot.edit_message_text(chat_id=MAIN_ADMIN,
                                message_id=message.message.message_id,
                                text=get_mes("confirm_deal_mes", deal=deal),
                                reply_markup=Keyboards.descision_deal_freezing(deal_id=deal.id))


@router.callback_query(F.data.contains("cancel_freezed_deal_"), IsAdmin())
async def confirm_freezed_deal(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    deal_id = int(message.data.replace("confirm_freezed_deal_", ""))
    deal = await deals.get(id=deal_id)
    deal.payment_status = 4
    await deals.update(deal=deal)
    await state.set_state(AdminStates.enter_buyer_wallet)
    deal_st = Deal_(id=deal.id, price=deal.price, user_id=deal.buyer_id)
    await state.update_data(deal=deal_st)
    await bot.send_message(chat_id=SELLER,
                                text=get_mes("notify_seller_cancel_deal", deal=deal),
                                )
    
    await bot.edit_message_text(chat_id=MAIN_ADMIN,
                                message_id=message.message.message_id,
                                text=get_mes("enter_buyer_wallet", deal=deal),
                                reply_markup=Keyboards.descision_deal_freezing(deal_id=deal.id))
    
@router.message(AdminStates.enter_buyer_wallet)
async def confirm_freezed_deal(message: Message, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    deal_st:Deal_ = data["deal"]
    deal = await deals.get(id=deal_st.id)
    accs =  await accounts.get_by_deal_id(deal.id)
    for acc in accs:
        acc.view_type = False
        await accounts.update(acc)
    #TODO: метод отправки денег покупателю
    await bot.send_message(chat_id=deal.buyer_id,
                                text=get_mes("notify_buyer_cancel_deal", deal=deal),
                                reply_markup=Keyboards.support_kb)
    
    await bot.send_message(chat_id=MAIN_ADMIN,
                                text=get_mes("end_cancel_deal", deal=deal),
                                reply_markup=Keyboards.descision_deal_freezing(deal_id=deal.id))
    await state.clear()


defect_accs_rt = router