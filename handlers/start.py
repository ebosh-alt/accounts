from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

from data.config import bot
from service.GetMessage import get_mes
from states.states import UserStates, Registration

router = Router()


@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await bot.send_message(get_mes("start"))
    await state.set_state(UserStates.registration)
    await state.update_data(registration=Registration())
    data = await state.get_data()
    registration = data["registration"]
    registration.user_id = message.from_user.id

start_rt = router
