from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from data.config import bot
from filters.Filters import IsAdmin
from models.database import deals, sellers
from service.GetMessage import get_mes
from service.keyboards import Keyboards
from states.states import AdminStates

router = Router()


@router.message(Command("admin"), IsAdmin())
async def admin(message: Message | CallbackQuery, state: FSMContext):
    await state.clear()
    await message.answer(text=get_mes("admin"), reply_markup=Keyboards.admin_kb)


# @router.callback_query(F.data.in_(), IsAdmin())
@router.callback_query(F.data == "show_deals", IsAdmin())
async def show_deals(message: CallbackQuery):
    all_deals = await deals.get_deals()


@router.callback_query(F.data == "show_seller_info", IsAdmin())
async def show_seller_info(message: CallbackQuery):
    try:
        seller = await sellers.get()
        await bot.send_message(chat_id=message.message.chat.id,
                               text=get_mes("seller_info",
                                            user_id=seller.id,
                                            balance=seller.balance,
                                            rating=seller.rating,
                                            username=seller.username
                                            ))
    except Exception as er:
        print(er)
        await bot.send_message(chat_id=message.message.chat.id, text=get_mes("seller_info_er", er=er))


@router.callback_query(F.data == "cancel_buy", IsAdmin())
async def cancel_buy_1(message: CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=message.message.chat.id, text=get_mes("input_DealId_admin"))
    await state.set_state(AdminStates().cancel_buy)


@router.message(AdminStates.cancel_buy, IsAdmin())
async def cancel_buy_end(message: Message | CallbackQuery, state: FSMContext):
    await state.clear()
    if message.text.isdigit():
        deal_id = int(message.text)
        if await deals.in_(deal_id):
            deal = await deals.get(id=deal_id)
            deal.payment_status = 2
            await deals.update(deal)
            return await message.answer(text=get_mes("seccess_cancel_buy"))
    await message.answer(text=get_mes("err_cancel_buy"))


admin_rt = router
