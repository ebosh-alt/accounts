from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from data.config import bot, Config
from filters.Filters import IsAdmin
from service.GetMessage import get_mes
from service.keyboards import Keyboards
from states.states import AdminStates

from aiogram.enums import ParseMode

router = Router()



@router.callback_query(F.data == "add_acc_type", IsAdmin())
async def add_acc_type(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    cfg = Config()
    cfg.load_config()
    await state.set_state(AdminStates.enter_new_acc_type)    
    await bot.send_message(chat_id=id,
                           text=get_mes("add_acc_type_1", acc_types=cfg.acceptable_account_types),
                           reply_markup=Keyboards.admin_back_menu_kb,
                           parse_mode=ParseMode.MARKDOWN_V2,

                           )


@router.message(AdminStates.enter_new_acc_type, IsAdmin())
async def add_acc_type_enter(message: Message, state: FSMContext):
    id = message.from_user.id
    cfg = Config()
    cfg.load_config()
    if message.text in cfg.acceptable_account_types:
        pass
    else:
        cfg.acceptable_account_types.append(message.text)
        cfg.save_config()
    await state.clear()
    await bot.send_message(chat_id=id,
                           text=get_mes("add_acc_type_success", acc_types=cfg.acceptable_account_types),
                           reply_markup=Keyboards.admin_back_menu_kb,
                           parse_mode=ParseMode.MARKDOWN_V2,
                           )



@router.callback_query(F.data == "delete_acc_type", IsAdmin())
async def delete_acc_type(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    await state.set_state(AdminStates.enter_acc_type_to_del)
    cfg = Config()
    cfg.load_config()
    await bot.send_message(chat_id=id,
                           text=get_mes("delete_acc_type_1", acc_types=cfg.acceptable_account_types),
                           reply_markup=Keyboards.admin_back_menu_kb,
                           parse_mode=ParseMode.MARKDOWN_V2,
                           )
    



@router.message(AdminStates.enter_acc_type_to_del, IsAdmin())
async def delete_acc_type_enter(message: Message, state: FSMContext):
    id = message.from_user.id
    cfg = Config()
    cfg.load_config()
    if message.text in cfg.acceptable_account_types:
        cfg.acceptable_account_types.remove(message.text)
        cfg.save_config()
    else:
        pass
    await state.clear()
    await bot.send_message(chat_id=id,
                           text=get_mes("delete_acc_type_success", acc_types=cfg.acceptable_account_types),
                           reply_markup=Keyboards.admin_back_menu_kb,
                           parse_mode=ParseMode.MARKDOWN_V2,
                           )



acc_types_rt = router
