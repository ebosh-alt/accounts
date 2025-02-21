from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from internal.app.app import bot
from internal.entities.database import acceptable_account_categories, AcceptableAccountCategory
from internal.filters.Filters import IsAdmin
from service.GetMessage import get_mes
from service.keyboards import Keyboards
from internal.entities.states.states import AdminStates

router = Router()


@router.callback_query(F.data == "add_acc_type", IsAdmin())
async def add_acc_type(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    await state.set_state(AdminStates.enter_new_acc_type)
    acceptable_account_names = await acceptable_account_categories.get_all_name_types()
    await bot.send_message(chat_id=id,
                           text=get_mes("add_acc_type_1", acc_types=acceptable_account_names),
                           reply_markup=Keyboards.admin_back_menu_kb,
                           parse_mode=ParseMode.MARKDOWN_V2,

                           )


@router.message(AdminStates.enter_new_acc_type, IsAdmin())
async def add_acc_type_enter(message: Message, state: FSMContext):
    id = message.from_user.id
    # cfg = Config()
    cfg = None
    acceptable_account_names = await acceptable_account_categories.get_all_name_types()

    if message.text in acceptable_account_names:
        pass
    else:
        await acceptable_account_categories.new(AcceptableAccountCategory(
            name=message.text
        ))
    acceptable_account_names = await acceptable_account_categories.get_all_name_types()

    # cfg.acceptable_account_types.append(message.text)
    # cfg.save_config()
    await state.clear()
    await bot.send_message(chat_id=id,
                           text=get_mes("add_acc_type_success", acc_types=acceptable_account_names),
                           reply_markup=Keyboards.admin_back_menu_kb,
                           parse_mode=ParseMode.MARKDOWN_V2,
                           )


@router.callback_query(F.data == "delete_acc_type", IsAdmin())
async def delete_acc_type(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    await state.set_state(AdminStates.enter_acc_type_to_del)
    # cfg = Config()
    acceptable_account_names = await acceptable_account_categories.get_all_name_types()
    await bot.send_message(chat_id=id,
                           text=get_mes("delete_acc_type_1", acc_types=acceptable_account_names),
                           reply_markup=Keyboards.admin_back_menu_kb,
                           parse_mode=ParseMode.MARKDOWN_V2,
                           )


@router.message(AdminStates.enter_acc_type_to_del, IsAdmin())
async def delete_acc_type_enter(message: Message, state: FSMContext):
    id = message.from_user.id
    acceptable_account_names = await acceptable_account_categories.get_all_name_types()

    if message.text in acceptable_account_names:
        acceptable = await acceptable_account_categories.get_by_name(message.text)
        await acceptable_account_categories.delete(acceptable)
    else:
        pass
    acceptable_account_names = await acceptable_account_categories.get_all_name_types()

    await state.clear()
    await bot.send_message(chat_id=id,
                           text=get_mes("delete_acc_type_success", acc_types=acceptable_account_names),
                           reply_markup=Keyboards.admin_back_menu_kb,
                           parse_mode=ParseMode.MARKDOWN_V2,
                           )


acc_types_rt = router
