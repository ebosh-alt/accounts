from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile, Document

from data.config import bot
from filters.Filters import IsManager
from service.GetMessage import get_mes
from service.keyboards import Keyboards
from states.states import ManagerStates
from data.config import EXCEL_TEMPLATE_PATH, EXCEL_LOAD_FILE_PATH
from service.ExcelS.s import create_accounts

router = Router()


@router.callback_query(F.data == "load_accs")
async def load_accs_1(message: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(
        chat_id=message.message.chat.id,
        message_id=message.message.message_id,
        text=get_mes("load_acc_1"),
        reply_markup=Keyboards.manager_back_menu_kb,
    )
    await bot.send_document(
        chat_id=message.message.chat.id,
        document=FSInputFile(EXCEL_TEMPLATE_PATH)
    )
    await state.set_state(ManagerStates().get_excel_file)


@router.message(ManagerStates.get_excel_file, IsManager(), F.document)
async def load_accs_end(message: Message, state: FSMContext):
    try:
        if type(message.document) is Document:
            document = message.document
        elif len(message.document) > 1:
            document = message.document[-1]
        file_type = document.file_name.split(".")[-1]
        if file_type == "xlsx":  # Проверка на тип файла
            path = f"{EXCEL_LOAD_FILE_PATH}/{document.file_name}"
            await bot.download(
                file=document,
                destination=path
            )
            await create_accounts(file_name=path)
            await bot.send_message(
                chat_id=message.chat.id,
                text=get_mes("success_loading_accs"),
                reply_markup=Keyboards.manager_menu_load_kb
            )
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=get_mes("err_loading_accs"),
                reply_markup=Keyboards.manager_menu_load_kb
            )
    except Exception as er:
        print(er)
        await bot.send_message(
            chat_id=message.chat.id,
            text=get_mes("err_loading_accs"),
            reply_markup=Keyboards.manager_menu_load_kb
        )
    await state.clear()


accounts_rt = router
