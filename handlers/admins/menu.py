from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from data.config import bot
from filters.Filters import IsAdmin
from service.GetMessage import get_mes
from service.keyboards import Keyboards

router = Router()


@router.callback_query(F.data == "admin_back_menu")
@router.message(Command("admin"), IsAdmin())
async def admin(message: Message | CallbackQuery, state: FSMContext):
    await state.clear()
    if type(message) is Message:
        await message.answer(
            text=get_mes("admin"),
            reply_markup=Keyboards.admin_menu_kb
        )
    else:
        await bot.edit_message_text(
            chat_id=message.message.chat.id,
            message_id=message.message.message_id,
            text=get_mes("admin"),
            reply_markup=Keyboards.admin_menu_kb
        )


admin_rt = router
