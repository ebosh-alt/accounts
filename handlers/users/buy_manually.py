import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from data.config import bot, client_s, SELLER, BOT_ID, BASE_PERCENT, PERCENT_GUARANTOR, ExNode, MERCHANT_ID, LIMIT_PRICE
from filters.Filters import IsUserMessageValid
from models.database import chats, Chat, deals, accounts, sellers
from models.models import CreatedOrder, ReceivedOrder
from service.GetMessage import get_mes, rounding_numbers
from service.date import format_date
from service.keyboards import Keyboards
from states.states import UserStates

logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data.in_(("Написать продавцу", "Общение с продавцом")))
async def start_mailing_to_seller(message: CallbackQuery, state: FSMContext):
    user_id = message.from_user.id
    await state.set_state(UserStates.MailingSeller)
    chat = await chats.get_chat_by_user(user_id=user_id)
    logger.info(chat)
    if chat is None:
        chat_id, er = await client_s.createChat([SELLER, int(BOT_ID)], title=str(user_id))
    else:
        chat_id = chat.id
        er = False

    if not er:
        if chat is None:
            chat = Chat(
                id=-chat_id,
                user_id=user_id,
                seller_id=SELLER,
            )
            await chats.new(chat=chat)
        await message.message.delete()
        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_mes("start_mailing_seller")
        )
    else:
        await bot.send_message(chat_id=user_id,
                               text="Произошла ошибка!\nНапишите в поддержку",
                               reply_markup=Keyboards.support_kb,
                               parse_mode=None)



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
    deal_id = int(message.data.replace("payment_manually_", ""))
    deal = await deals.get(deal_id)
    # deal = await deals.get_last_deal(user_id=id)
    accs = await accounts.get_by_deal_id(deal.id)
    account = accs[0]
    if deal.guarantor:
        price = rounding_numbers("%.2f" % (account.price * (1 + PERCENT_GUARANTOR / 100)))
    else:
        price = rounding_numbers("%.2f" % (account.price * (1 + BASE_PERCENT / 100)))
    if price < LIMIT_PRICE:
        await message.answer(f"Сумма минимального заказа {LIMIT_PRICE} USDT. "
                             f"Стоимость покупки изменена до минимальной стоимости",
                             show_alert=True)
        price = LIMIT_PRICE
        # await state.update_data(ShoppingCart=shopping_cart)
    # invoice = CryptoCloud.create_invoice(amount=price)
    # uuid = invoice["result"]["uuid"]
    # link = invoice["result"]["link"]
    order: CreatedOrder = await ExNode.create_order(client_transaction_id=str(deal.id),
                                                    amount=float(price),
                                                    merchant_uuid=MERCHANT_ID)
    # shopping_cart.tracker_id = order.tracker_id
    if order.date_expire:
        date_expire = format_date(order.date_expire)
        await bot.edit_message_text(chat_id=id,
                                    message_id=message.message.message_id,
                                    text=get_mes("receiver", price=price, receiver=order.receiver, date_expire=date_expire),
                                    reply_markup=await Keyboards.payment())
    else:
        await bot.edit_message_text(chat_id=id,
                                    message_id=message.message.message_id,
                                    text=get_mes("receiver", price=price, receiver=order.receiver),
                                    reply_markup=await Keyboards.payment())
    await state.set_state(UserStates.Manually)
    await state.update_data(deal_id=deal_id)
    await state.update_data(tracker_id=order.tracker_id)


@router.callback_query(UserStates.Manually, F.data == "complete_payment")
async def complete_payment(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    deal_id = data["deal_id"]
    tracker_id = data["tracker_id"]
    received_order: ReceivedOrder = await ExNode.get_order(tracker_id=tracker_id)
    if received_order.status == "SUCCESS":
        deal = await deals.get(deal_id)
        accs = await accounts.get_by_deal_id(deal.id)
        account = accs[0]
        await bot.edit_message_text(chat_id=id,
                                    message_id=message.message.message_id,
                                    text=account.data,
                                    reply_markup=Keyboards.support_kb)
        seller = await sellers.get()
        if deal.guarantor is False:
            text = get_mes("mark_seller")
            keyboard = Keyboards.mark_seller_kb
            deal.payment_status = 2
            seller.balance += account.price
            seller = await sellers.get()
            await bot.send_message(chat_id=seller.id,
                                   test=get_mes("complete_payment",
                                                user_id=id,
                                                deal_id=deal.id,
                                                amount=account.price,
                                                guarantor="без гаранта")
                                   )
        else:
            text = get_mes("support_24_hours")
            keyboard = await Keyboards.confirm_account_user_kb(deal.id)
            deal.payment_status = 1
            await bot.send_message(chat_id=seller.id,
                                   test=get_mes("complete_payment",
                                                user_id=id,
                                                deal_id=deal.id,
                                                amount=account.price,
                                                guarantor="с гарантом")
                                   )

        await deals.update(deal)
        await bot.send_message(chat_id=id,
                               text=text,
                               reply_markup=keyboard)
        await state.clear()
    else:
        await message.answer("Счет ещё не оплачен! Не уходите с этого этапа")


buy_manually_rt = router
