from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config.config import config
from internal.app.app import bot

from service.GetMessage import get_mes
from service.keyboards import Keyboards
from internal.entities.states.states import AdminStates

router = Router()




@router.callback_query(F.data.in_(["change_name_shop", "change_description_seller"]))
async def change_name_shop(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    # kb =/ None
    if id == config.manager.seller_id:
        kb = Keyboards.manager_back_menu_kb
    elif id in config.admin.ids:
        kb = Keyboards.admin_back_menu_kb
    else:
        await bot.edit_message_text(chat_id=id,
                                    message_id=message.message.message_id,
                                    text="Произошла ошибка")
        return

    if message.data == "change_name_shop":
        change = "change_name_shop"
        text = get_mes("change_name_shop")
    elif message.data == "change_description_seller":
        change = "change_description_seller"
        text = get_mes("change_description_seller")
    else:
        await bot.edit_message_text(chat_id=id,
                                    message_id=message.message.message_id,
                                    text="Произошла ошибка",
                                    reply_markup=kb)
        return

    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=text,
                                reply_markup=kb)
    await state.set_state(AdminStates().change_about_shop)
    await state.update_data(message_id=message.message.message_id, change=change)


@router.message(AdminStates.change_about_shop)
async def set_name_shop(message: Message, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    message_id = data["message_id"]
    change = data["change"]
    text = message.text
    # config = Config()
    config = None
    kb = None
    if id == config.manager.seller_id:
        kb = Keyboards.manager_back_menu_kb
    elif id in config.admin.ids:
        kb = Keyboards.admin_back_menu_kb
    if change == "change_name_shop":
        config.name_shop = text
    elif change == "change_description_seller":
        config.description_seller = text
    config.save_config()
    await message.delete()

    await bot.edit_message_text(chat_id=id,
                                message_id=message_id,
                                text="Параметр обновлен",
                                reply_markup=kb)
    await state.clear()


about_shop_rt = router