from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from data.config import bot
from filters.Filters import IsManager
from service.GetMessage import get_mes
from service.keyboards import Keyboards
from states.states import ManagerStates

router = Router()

@router.callback_query(F.data == "manager_back_menu")
@router.message(Command("manager"), IsManager())
async def admin(message: Message | CallbackQuery, state: FSMContext):
    if type(message) is Message:
        await message.answer(
            text=get_mes("manager"), 
            reply_markup=Keyboards.manager_menu_kb
            )
    elif await state.get_state() == ManagerStates().get_excel_file:
        await bot.delete_message(
            chat_id=message.message.chat.id,
            message_id=message.message.message_id,
        )
        await bot.send_message(
            chat_id=message.message.chat.id,
            text=get_mes("manager"),
            reply_markup=Keyboards.manager_menu_kb
        )
    else:
        await bot.edit_message_text(
                chat_id=message.message.chat.id,
                message_id=message.message.message_id,
                text=get_mes("manager"),
                reply_markup=Keyboards.manager_menu_kb
            )
    await state.clear()


manager_rt = router
