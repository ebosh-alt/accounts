from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from data.config import bot
from filters.Filters import IsAdmin
from models.database import deals, Deal
from models.models import DataDeals
from service.GetMessage import get_mes
from service.keyboards import Keyboards
from states.states import AdminStates
from service import SendDeals

router = Router()


@router.callback_query(F.data == "show_deals", IsAdmin())
async def show_deals(message: CallbackQuery):
    all_data_deals = await deals.get_data_deals()
    if len(all_data_deals) == 0:
        return await bot.edit_message_text(
            chat_id=message.message.chat.id,
            message_id=message.message.message_id,
            text="Пока ничего нет",
            reply_markup=Keyboards.admin_back_menu_kb
        )
    await SendDeals.send(
        message=message,
        all_data_deals=all_data_deals,
        keyboard=Keyboards.admin_menu_kb
    )


@router.callback_query(F.data == "cancel_buy", IsAdmin())
async def cancel_buy_1(message: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(
        chat_id=message.message.chat.id,
        message_id=message.message.message_id,
        text=get_mes("input_DealId_admin"),
        reply_markup=Keyboards.admin_back_menu_kb
    )
    await state.set_state(AdminStates().cancel_buy)


@router.message(AdminStates.cancel_buy, IsAdmin())
async def cancel_buy_end(message: Message | CallbackQuery, state: FSMContext):
    await state.clear()
    if message.text.isdigit():
        deal_id = int(message.text)
        if await deals.in_(deal_id):
            deal: Deal = await deals.get(id=deal_id)
            deal.payment_status = 2
            await deals.update(deal)
            return await message.answer(
                text=get_mes("success_cancel_buy"),
                reply_markup=Keyboards.admin_menu_kb
            )
    await message.answer(
        text=get_mes("err_cancel_buy"),
        reply_markup=Keyboards.admin_menu_kb
    )


deals_rt = router
