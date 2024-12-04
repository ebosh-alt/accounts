from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message

from data.config import EXCEL_TEMPLATE_PATH_REPLACE_CHANGE, EXCEL_TEMPLATE_PATH_DELETE, logging, EXCEL_LOAD_FILE_PATH
from data.config import bot
from filters.Filters import IsManager
from models.database import accounts
from service.GetMessage import get_mes
from service.keyboards import Keyboards
from states.states import ManagerStates

router = Router()

logger = logging.getLogger(__name__)


@router.callback_query(F.data == "work_catalog")
async def load_accs_1(message: CallbackQuery):
    await bot.edit_message_text(
        chat_id=message.message.chat.id,
        message_id=message.message.message_id,
        text="Выберите действие",
        reply_markup=Keyboards.manager_loads_accs_tree_kb,
    )


@router.callback_query(F.data == "replace_catalog")
async def new_catalog(message: CallbackQuery, state: FSMContext):
    await state.set_state(ManagerStates().replace_catalog)
    await bot.edit_message_text(
        chat_id=message.message.chat.id,
        message_id=message.message.message_id,
        text=get_mes("replace_catalog"),
        reply_markup=Keyboards.manager_back_menu_kb,
    )

    await bot.send_document(
        chat_id=message.message.chat.id,
        document=FSInputFile(EXCEL_TEMPLATE_PATH_REPLACE_CHANGE)
    )


@router.callback_query(F.data == "change_catalog")
async def change_catalog(message: CallbackQuery, state: FSMContext):
    await state.set_state(ManagerStates().change_catalog)

    await bot.edit_message_text(
        chat_id=message.message.chat.id,
        message_id=message.message.message_id,
        text=get_mes("change_catalog"),
        reply_markup=Keyboards.manager_back_menu_kb,
    )


@router.callback_query(F.data == "delete_from_catalog")
async def delete_from_catalog(message: CallbackQuery, state: FSMContext):
    await state.set_state(ManagerStates().delete_from_catalog)
    await bot.edit_message_text(
        chat_id=message.message.chat.id,
        message_id=message.message.message_id,
        text=get_mes("delete_from_catalog"),
        reply_markup=Keyboards.manager_back_menu_kb,
    )
    await bot.send_document(
        chat_id=message.message.chat.id,
        document=FSInputFile(EXCEL_TEMPLATE_PATH_DELETE)
    )


@router.message(ManagerStates.replace_catalog, IsManager(), F.document)
@router.message(ManagerStates.change_catalog, IsManager(), F.document)
@router.message(ManagerStates.delete_from_catalog, IsManager(), F.document)
async def load_accs_end(message: Message, state: FSMContext):
    try:
        document = message.document
        user_state = await state.get_state()
        if not document.file_name.endswith(".xlsx"):
            await bot.send_message(
                chat_id=message.chat.id,
                text=get_mes("err_loading_accs"),
                reply_markup=Keyboards.manager_back_menu_kb
            )
            return
        file_path = f"{EXCEL_LOAD_FILE_PATH}/{document.file_name}"
        await bot.download(
            file=document,
            destination=file_path
        )
        response = None
        match user_state:
            case ManagerStates.replace_catalog:
                response = await accounts.replace_catalog(file_path)
            case ManagerStates.change_catalog:
                response = await accounts.change_catalog(file_path)
            case ManagerStates.delete_from_catalog:
                response = await accounts.delete_from_catalog(file_path)
        if response:
            if response.status == 200:
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=get_mes("success_loading_accs"),
                    reply_markup=Keyboards.manager_back_menu_kb
                )
            else:
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=get_mes("err_loading_accs"),
                    reply_markup=Keyboards.manager_back_menu_kb
                )
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=get_mes("err_loading_accs"),
                reply_markup=Keyboards.manager_back_menu_kb
            )
    except Exception as er:
        logger.info(er)
        await bot.send_message(
            chat_id=message.chat.id,
            text=get_mes("err_loading_accs"),
            reply_markup=Keyboards.manager_back_menu_kb
        )
    await state.clear()

accounts_rt = router
