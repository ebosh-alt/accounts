from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from data.config import bot
from filters.Filters import IsAdmin
from models.database import deals
from models.database.data_deals import DataDeals
from service.GetMessage import get_mes
from service.keyboards import Keyboards
from states.states import AdminStates


router = Router()

async def send_data_deals(message: CallbackQuery, all_data_deals: list[DataDeals], fmes_text_path: str, keyboard):
    '''service.GetMessage.get_mes() использует в качестве аргумента fmes_text_path\n
    fmes_text_path - название файла .md\n
    get_mes(fmes_text_path)'''
    ind = 0
    new_data = list()
    count_symb=0
    while  ind<len(all_data_deals):
        count_symb += all_data_deals[ind].len() + 130
        if count_symb < 2000:
            new_data.append(all_data_deals[ind])
        else:
            await bot.send_message(
                chat_id=message.message.chat.id,
                text=get_mes("history_buy_user", deals=new_data),
            )
            count_symb = 0
            new_data = list()
            new_data.append(all_data_deals[ind])
        ind+=1
    if len(new_data) != 0:
        print("HEY")
        await bot.send_message(
                chat_id=message.message.chat.id,
                text=get_mes("history_buy_user", deals=new_data),
            )
    await bot.send_message(
                chat_id=message.message.chat.id,
                text=get_mes(fmes_text_path), 
                reply_markup=keyboard
            )
    
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
    await send_data_deals(
        message=message,
        all_data_deals=all_data_deals,
        fmes_text_path="admin",
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
            deal = await deals.get(id=deal_id)
            deal.payment_status = 2
            await deals.update(deal)
            return await message.answer(
                text=get_mes("seccess_cancel_buy"),
                reply_markup=Keyboards.admin_menu_kb
                )     
    await message.answer(
        text=get_mes("err_cancel_buy"),
        reply_markup=Keyboards.admin_menu_kb
        )



deals_rt = router
