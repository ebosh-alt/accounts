from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from data.config import bot
from service.GetMessage import get_mes

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    await bot.send_message(get_mes("start"))


start_rt = router
