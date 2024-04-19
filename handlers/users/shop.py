from datetime import datetime
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from models.database import users, accounts, deals, Deal, Account, sellers, Seller
from data.config import bot
from service import keyboards as kb
from service.GetMessage import get_mes
from service.keyboards import Keyboards as kb

router = Router()


@router.callback_query(F.data == "shop")
async def shop_callback(message: CallbackQuery):
    id = message.from_user.id
    print(await accounts.get_shop())


shop_rt = router
