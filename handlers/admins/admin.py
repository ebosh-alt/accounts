from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from data.config import bot
from service.GetMessage import get_mes
from states.states import UserStates
from filters.Filters import IsAdmin
from service.keyboards import Keyboards
from models.DatabaseModels import Deals, Sellers
from models.StateModels import Score
from states.states import AdminStates
from models.db import session_db
from sqlalchemy.ext.asyncio import AsyncSession


router = Router()


@router.message(Command("admin"), IsAdmin())
async def admin(message: Message | CallbackQuery, state: FSMContext):
    await state.clear()
    await message.answer(text=get_mes("admin"),reply_markup=Keyboards.admin_kb)

@session_db
# @router.callback_query(F.data.in_(), IsAdmin())
@router.callback_query(F.data == "show_deals", IsAdmin())
async def show_deals(message: CallbackQuery):
    deals = await Deals.get_all()


@router.callback_query(F.data == "show_seller_info", IsAdmin())
@session_db
async def show_seller_info(message: CallbackQuery, session: AsyncSession):
    try:
        seller:Sellers = await Sellers.obj(session=session)
        await bot.send_message(chat_id=message.message.chat.id, text=get_mes("seller_info", user_id=seller.id, balance=seller.balance, rating=seller.rating, username=seller.username))
    except Exception as er:
        print(er)
        await bot.send_message(chat_id=message.message.chat.id, text=get_mes("seller_info_er", er=er))


@router.callback_query(F.data == "cancel_buy", IsAdmin())
@session_db
async def cancel_buy_1(message: CallbackQuery, state: FSMContext, session: AsyncSession):
    await bot.send_message(chat_id=message.message.chat.id, text=get_mes("input_DealId_admin"))
    await state.set_state(AdminStates().cancel_buy)


@router.message(AdminStates.cancel_buy, IsAdmin())
@session_db
async def cancel_buy_end(message: Message | CallbackQuery, session: AsyncSession, state: FSMContext):
    await state.clear()
    if (message.text).isdigit():
        deal_id = int(message.text)
        if await Deals.is_register(deal_id, session=session):
            deal = await Deals.obj(id=deal_id, session=session)
            deal.payment_status = 2
            await session.commit()
            return await message.answer(text=get_mes("seccess_cancel_buy"))
    await message.answer(text=get_mes("err_cancel_buy"))

        
            

        


admin_rt = router
