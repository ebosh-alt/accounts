import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from data.config import bot, client_s, SELLER, BOT_ID, CryptoCloud, PERCENT, BASE_PERCENT
from filters.Filters import IsUserMessageValid
from models.database import chats, Chat, deals, accounts, sellers
from service.GetMessage import get_mes
from states.states import UserStates
from service.keyboards import Keyboards

logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data == "Общение с продавцом")
async def start_mailing_to_seller(message: CallbackQuery, state: FSMContext):
    user_id = message.from_user.id
    await state.set_state(UserStates.MailingSeller)
    # Создание чата
    chat = await chats.get_chat_by_user(user_id=user_id)
    if chat is None:
        chat_id, er = await client_s.createChat([SELLER, int(BOT_ID)], title=str(user_id))
    else:
        chat_id = chat.id
        er = True
    if not er:
        chat = Chat(
            id=-chat_id,
            user_id=user_id,
            seller_id=SELLER,
        )
        await chats.new(chat=chat)
    await message.delete()
    await bot.send_message(
        chat_id=message.from_user.id,
        # message_id=message.message.message_id,
        text=get_mes("start_mailing_seller")
    )


@router.message(UserStates.MailingSeller, IsUserMessageValid())
async def send_message_seller(message: Message, state: FSMContext):
    chat = await chats.get_chat_by_user(user_id=message.from_user.id)
    if chat is not None:
        await bot.send_message(
            chat_id=chat.id,
            text=message.text,
        )
    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_mes("err_send_text_manager"),
        )


@router.callback_query(F.data.contains("payment_manually_"))
async def payment(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    deal = await deals.get_last_deal(user_id=id)
    account = await accounts.get(deal.account_id)
    if deal.guarantor:
        price = float("%.2f" % (account.price * (1 + BASE_PERCENT / 100) * (1 + PERCENT / 100)))
    else:
        price = float("%.2f" % (account.price * (1 + BASE_PERCENT / 100)))
    invoice = CryptoCloud.create_invoice(amount=price)
    uuid = invoice["result"]["uuid"]
    link = invoice["result"]["link"]
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("rule_payment"),
                                reply_markup=await Keyboards.payment(link))
    await state.set_state(UserStates.Manually)
    deal_id = int(message.data.replace("payment_manually_", ""))
    await state.update_data(deal_id=deal_id)
    await state.update_data(uuid=uuid)


@router.callback_query(UserStates.Manually, F.data == "complete_payment")
async def complete_payment(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    deal_id = data["deal_id"]
    uuid = data["uuid"]
    invoice = CryptoCloud.get_invoice_info([uuid])
    if invoice["result"][0]["status"] == "paid":
        deal = await deals.get(deal_id)
        account = await accounts.get(deal.account_id)
        await bot.edit_message_text(chat_id=id,
                                    message_id=message.message.message_id,
                                    text=account.data,
                                    reply_markup=Keyboards.support_kb)

        if deal.guarantor is False:
            text = get_mes("mark_seller")
            keyboard = Keyboards.mark_seller_kb
            deal.payment_status = 2
            seller = await sellers.get()
            seller.balance += account.price
        else:
            text = get_mes("support_24_hours")
            keyboard = Keyboards.confirm_account_user_kb
            deal.payment_status = 1

        await deals.update(deal)
        await bot.send_message(chat_id=id,
                               text=text,
                               reply_markup=keyboard)
    else:
        await message.answer("Счет ещё не оплачен! Не уходите с этого этапа")


@router.callback_query(UserStates.Manually, F.data == "ok_account")
async def complete_payment(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()

    deal_id = data['deal_id']
    deal = await deals.get(deal_id)
    deal.payment_status = 2
    account = await accounts.get(deal.account_id)
    seller = await sellers.get()
    seller.balance += account.price
    await deals.update(deal)
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("mark_seller"),
                                reply_markup=Keyboards.mark_seller_kb)


@router.callback_query((F.data == "0") | (F.data == "1"))
async def set_mark(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    mark = int(message.data)
    seller = await sellers.get()
    seller.rating += mark
    await sellers.update(seller)
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text="Спасибо за оценку!",
                                reply_markup=Keyboards.confirm_payment_kb)

    await state.clear()


buy_manually_rt = router
