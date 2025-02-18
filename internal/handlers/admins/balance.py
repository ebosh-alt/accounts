from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from internal.app.app import bot
from internal.filters.Filters import IsAdmin
from internal.entities.database import sellers
from service.GetMessage import get_mes
from service.is_float import is_float
from service.keyboards import Keyboards
from internal.entities.states.states import AdminStates

router = Router()


@router.callback_query(F.data == "change_balance")
async def admin(message: Message | CallbackQuery, state: FSMContext):
    id = message.from_user.id
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("change_balance"),
                                reply_markup=Keyboards.admin_back_menu_kb)
    await state.set_state(AdminStates.change_balance)
    await state.update_data(message_id=message.message.message_id)


@router.message(IsAdmin(), AdminStates.change_balance)
async def change_balance(message: Message | CallbackQuery, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    message_id = data["message_id"]
    await message.delete()
    if is_float(message.text):
        seller = await sellers.get()
        seller.balance -= float(message.text)
        await sellers.update(seller)
        await bot.edit_message_text(chat_id=id,
                                    message_id=message_id,
                                    text=get_mes("change_balance_complete"),
                                    reply_markup=Keyboards.admin_menu_kb)
        await state.clear()
    else:
        await bot.edit_message_text(chat_id=id,
                                    message_id=message_id,
                                    text=get_mes("err_cancel_err"),
                                    reply_markup=Keyboards.admin_menu_kb
                                    )


balance_rt = router
