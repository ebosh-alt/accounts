from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

from data.config import bot
from service.GetMessage import get_mes
from states.states import UserStates

router = Router()


@router.message(Command("admin"))
async def admin(message: Message, state: FSMContext):
    await bot.send_message(get_mes("start"))


admin_rt = router
