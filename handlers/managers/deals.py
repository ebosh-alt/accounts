from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile, Document, ForceReply
from aiogram.enums import ParseMode
from data.config import bot
from filters.Filters import IsManager
from service.GetMessage import get_mes
from service.keyboards import Keyboards
from states.states import ManagerStates
from data.config import EXCEL_TEMPLATE_PATH, EXCEL_LOAD_FILE_PATH
from service.ExcelS.s import create_accounts
from models.StateModels import Deal as Deal_
from models.database import accounts, Account, deals, Deal, users
from datetime import datetime

router = Router()


@router.callback_query(F.data == "create_deal")
async def create_deal_user_id(message: CallbackQuery, state: FSMContext):
    await state.set_state(ManagerStates.create_deal_user_id)
    await state.update_data(deal=Deal_())
    await bot.send_message(
        chat_id=message.message.chat.id,
        text=get_mes("create_deal_data_input", data="user\_id"),
        reply_markup=ForceReply(input_field_placeholder=get_mes("create_deal_input_text", data="user_id")),
        parse_mode=ParseMode.MARKDOWN_V2
        )
    

@router.message(ManagerStates.create_deal_user_id, IsManager())
async def create_deal_shop(message: Message, state: FSMContext):
    data: dict = await state.get_data()
    deal: Deal_ = data["deal"]
    if message.text.isdigit():
        if users.in_(id=int(message.text)):
            deal.user_id = int(message.text)
            await state.update_data(deal=deal)
            await state.set_state(ManagerStates.create_deal_shop)
            text = get_mes("create_deal_data_input", data="shop")
            keyboard = ForceReply(input_field_placeholder=get_mes("create_deal_input_text", data="shop"))
        else:
            text = get_mes("create_deal_data_input", er="Нет такого пользователя\!", data="user\_id")
            keyboard = ForceReply(input_field_placeholder=get_mes("create_deal_input_text", data="user_id"))
    else:
        text = get_mes("create_deal_data_input", er="Введите число\!", data="user\_id")
        keyboard = ForceReply(input_field_placeholder=get_mes("create_deal_input_text", data="user_id"))
    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN_V2
        )


@router.message(ManagerStates.create_deal_shop, IsManager())
async def create_deal_price(message: Message, state: FSMContext):
    data: dict = await state.get_data()
    deal: Deal_ = data["deal"]
    deal.shop = message.text
    await state.update_data(deal=deal)
    await state.set_state(ManagerStates.create_deal_price)
    await bot.send_message(
        chat_id=message.chat.id,
        text=get_mes("create_deal_data_input", data="price"),
        reply_markup=ForceReply(input_field_placeholder=get_mes("create_deal_input_text", data="price")),
        parse_mode=ParseMode.MARKDOWN_V2
        )
    

@router.message(ManagerStates.create_deal_price, IsManager())
async def create_deal_description(message: Message, state: FSMContext):
    data: dict = await state.get_data()
    deal: Deal_ = data["deal"]
    if message.text.isdigit():
        deal.price = int(message.text)
        await state.update_data(deal=deal)
        await state.set_state(ManagerStates.create_deal_description)
        text = get_mes("create_deal_data_input", data="description")
        keyboard = ForceReply(input_field_placeholder=get_mes("create_deal_input_text", data="description"))
    else:
        text = get_mes("create_deal_data_input", er="Введите число\!", data="price")
        keyboard = ForceReply(input_field_placeholder=get_mes("create_deal_input_text", data="price"))
    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN_V2
        )


@router.message(ManagerStates.create_deal_description, IsManager())
async def create_deal_data(message: Message, state: FSMContext):
    data: dict = await state.get_data()
    deal: Deal_ = data["deal"]
    deal.description = message.text
    await state.update_data(deal=deal)
    await state.set_state(ManagerStates.create_deal_data)
    await bot.send_message(
        chat_id=message.chat.id,
        text=get_mes("create_deal_data_input", data="data"),
        reply_markup=ForceReply(input_field_placeholder=get_mes("create_deal_input_text", data="data")),
        parse_mode=ParseMode.MARKDOWN_V2
        )
    

@router.message(ManagerStates.create_deal_data, IsManager())
async def create_deal_name(message: Message, state: FSMContext):
    data: dict = await state.get_data()
    deal: Deal_ = data["deal"]
    deal.data = message.text
    await state.update_data(deal=deal)
    await state.set_state(ManagerStates.create_deal_name)
    await bot.send_message(
        chat_id=message.chat.id,
        text=get_mes("create_deal_data_input", data="name"),
        reply_markup=ForceReply(input_field_placeholder=get_mes("create_deal_input_text", data="name")),
        parse_mode=ParseMode.MARKDOWN_V2
        )


@router.message(ManagerStates.create_deal_name, IsManager())
async def create_deal_guarant(message: Message, state: FSMContext):
    data: dict = await state.get_data()
    deal: Deal_ = data["deal"]
    deal.name = message.text
    await state.update_data(deal=deal)
    await state.set_state(ManagerStates.create_deal_guarant)
    await bot.send_message(
        chat_id=message.chat.id,
        text=get_mes("create_deal_data_input", data="guarant"),
        reply_markup=Keyboards.manager_deal_cr_choose_g_type,
        parse_mode=ParseMode.MARKDOWN_V2
        )


@router.callback_query(ManagerStates.create_deal_guarant, IsManager(), F.data == "cr_deal_g" or F.data == "cr_deal_not_g")
async def create_deal_confirm(message: CallbackQuery, state: FSMContext):
    data: dict = await state.get_data()
    deal: Deal_ = data["deal"]
    if  message.data == "cr_deal_g":    
        deal.guarant_type = True
    elif message.data == "cr_deal_not_g":
        deal.guarant_type = False
    await state.update_data(deal=deal)
    await state.set_state(ManagerStates.create_deal_end)
    await bot.send_message(
        chat_id=message.message.chat.id,
        text=get_mes("manager_confirm_cr_deal", deal = deal),
        reply_markup=Keyboards.manager_deal_cr_confirm,
        parse_mode=ParseMode.MARKDOWN_V2
        )


@router.callback_query(ManagerStates.create_deal_end, IsManager(), F.data == "cr_deal_success" or F.data == "cr_deal_unsuccess")
async def create_deal_end(message: CallbackQuery, state: FSMContext):
    data: dict = await state.get_data()
    deal: Deal_ = data["deal"]
    if  message.data == "cr_deal_success":  
        account = Account(
            shop = deal.shop,
            price = deal.price,
            description = deal.description,
            data = deal.data,
            view_type = False,
            name = deal.name
        )
        await accounts.new(account=account)
        account = await accounts.get_last()
        c_deal = Deal(
            buyer_id=deal.user_id,
            seller_id=message.message.chat.id,
            account_id=account.id,
            date=datetime.now(),
            guarantor=deal.guarant_type,
            payment_status=0,
        )
        await deals.new(c_deal)
        await bot.send_message(
            chat_id=deal.user_id,
            text=get_mes("created_deal_to_user", deal=deal),
            reply_markup=Keyboards.confirm_cr_deal_by_user,
            parse_mode=ParseMode.MARKDOWN_V2
            )        
    elif message.data == "cr_deal_unsuccess":
        pass
    await state.clear()
    await bot.send_message(
        chat_id=message.message.chat.id,
        text=get_mes("manager"),
        reply_markup=Keyboards.manager_menu_kb,
        parse_mode=ParseMode.MARKDOWN_V2
        )


deals_rt = router