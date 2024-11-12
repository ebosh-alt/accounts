import logging
from datetime import datetime

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from data.config import bot, BASE_PERCENT, PERCENT_GUARANTOR, ExNode, MERCHANT_ID, link_to_bot, LIMIT_PRICE
from filters.Filters import IsShop, IsNameAccount
from models.StateModels import ShoppingCart
from models.database import deals, accounts, sellers
from models.models import CreatedOrder, ReceivedOrder
from service import cryptography
from service.GetMessage import get_mes, rounding_numbers
from service.buy_automatically import set_data_shopping_cart, create_deal
from service.date import format_date
from service.keyboards import Keyboards
from states.states import UserStates

logger = logging.getLogger(__name__)
router = Router()

buy_automatically_rt = router


@router.callback_query(F.data.in_(("shop", "Вернуться к выбору магазина", "Вернуться к выбору действия")))
async def menu_shop(message: CallbackQuery, state: FSMContext):
    # главное меню покупки аккаунтов и выбор магазина
    id = message.from_user.id
    await message.message.delete()
    await bot.send_message(chat_id=id,
                           text=get_mes("shop_user"),
                           reply_markup=await Keyboards.choice_action())
    await state.clear()
    await state.set_state(UserStates.ShoppingCart)


@router.callback_query(F.data == "Перейти к выбору категорий", UserStates.ShoppingCart)
async def choose_shop(message: CallbackQuery):
    id = message.from_user.id
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("shop_user_categories"),
                                reply_markup=await Keyboards.shop_kb())


@router.callback_query(IsShop(), UserStates.ShoppingCart)
async def choose_after_shop_act(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    await set_data_shopping_cart(state=state, shop=message.data)
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("shop_user"),
                                reply_markup=await Keyboards.choice_action_name_account())


@router.callback_query(F.data.in_(("Перейти к выбору товаров", "Вернуться к выбору товаров")), UserStates.ShoppingCart)
async def choice_account(message: CallbackQuery, state: FSMContext):
    # выбор аккаунта и сохранение выбранного магазина
    id = message.from_user.id
    data = await state.get_data()
    shopping_cart = data["ShoppingCart"]
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text="Выберите товар",
                                reply_markup=await Keyboards.name_accounts_shop_kb(shop=shopping_cart.shop))


@router.callback_query(UserStates.ShoppingCart, IsNameAccount())
async def choice_guarantor(message: CallbackQuery | Message, state: FSMContext, shop: str = None, name: str = None):
    # сохранение имени выбранного аккаунта и выбор количества аккаунтов
    shopping_cart: ShoppingCart
    count_account: int
    id = message.from_user.id
    logger.info(f"{shop}, {name}")
    if name is None:
        name = message.data
    shopping_cart, count_account, acc = await set_data_shopping_cart(state, name=name, shop=shop)
    price_no = rounding_numbers("%.2f" % (acc.price * (1 + BASE_PERCENT / 100) * shopping_cart.count))
    price_yes = rounding_numbers("%.2f" % (acc.price * (1 + PERCENT_GUARANTOR / 100) * shopping_cart.count))
    link = f"{link_to_bot}?start={cryptography.encode(shopping_cart.shop + "%" + shopping_cart.name)}"
    reply_markup = await Keyboards.choice_count_account(count=count_account)
    text = get_mes("shopping_cart_user",
                   shop=shopping_cart.shop,
                   name=shopping_cart.name,
                   price_no=price_no,
                   price_yes=price_yes,
                   description=shopping_cart.description,
                   count=count_account,
                   choice_count=shopping_cart.count,
                   link=link
                   )
    if type(message) is Message:
        await bot.send_message(chat_id=id,
                               text=text,
                               reply_markup=reply_markup,
                               parse_mode=ParseMode.MARKDOWN_V2,
                               )
    else:
        await bot.edit_message_text(chat_id=id,
                                    message_id=message.message.message_id,
                                    text=text,
                                    reply_markup=reply_markup,
                                    parse_mode=ParseMode.MARKDOWN_V2,
                                    )


@router.callback_query(UserStates.ShoppingCart, F.data.in_(["add_account", "remove_account"]))
async def choice_count_account(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    shopping_cart: ShoppingCart = data['ShoppingCart']
    accs = await accounts.get_account_by_name(name=shopping_cart.name, shop=shopping_cart.shop)
    count_account = len(accs)
    if message.data == "add_account":
        if shopping_cart.count + 1 <= count_account:
            shopping_cart.count = shopping_cart.count + 1
        else:
            await message.answer("Вы выбрали максимум")
            return
    elif message.data == "remove_account":
        if shopping_cart.count - 1 >= 1:
            shopping_cart.count = shopping_cart.count - 1
        else:
            await message.answer("Вы выбрали минимум")
            return
    price_no = rounding_numbers("%.2f" % (accs[0].price * (1 + BASE_PERCENT / 100) * shopping_cart.count))
    price_yes = rounding_numbers("%.2f" % (accs[0].price * (1 + PERCENT_GUARANTOR / 100) * shopping_cart.count))
    link = f"{link_to_bot}?start={cryptography.encode(shopping_cart.shop + "%" + shopping_cart.name)}"
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("shopping_cart_user",
                                             shop=shopping_cart.shop,
                                             name=shopping_cart.name,
                                             price_no=price_no,
                                             price_yes=price_yes,
                                             description=shopping_cart.description,
                                             count=count_account,
                                             choice_count=shopping_cart.count,
                                             link=link
                                             ),
                                parse_mode=ParseMode.MARKDOWN_V2,
                                reply_markup=await Keyboards.choice_count_account(count=count_account))


@router.callback_query(UserStates.ShoppingCart, F.data.contains("guarantor"))
async def confirm_shopping_cart(message: CallbackQuery, state: FSMContext):
    # переход к оплате или отмена и сохранение с или без гаранта
    id = message.from_user.id
    shopping_cart: ShoppingCart = await set_data_shopping_cart(state, guarantor=message.data)

    link = f"{link_to_bot}?start={cryptography.encode(shopping_cart.shop + "%" + shopping_cart.name)}"
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("shopping_cart_user",
                                             shop=shopping_cart.shop,
                                             name=shopping_cart.name,
                                             price=rounding_numbers(str(shopping_cart.price)),
                                             description=shopping_cart.description,
                                             choice_count=shopping_cart.count,
                                             link=link
                                             ),
                                parse_mode=ParseMode.MARKDOWN_V2,
                                reply_markup=Keyboards.ready_payment_kb)


@router.callback_query(UserStates.ShoppingCart, F.data == "payment")
async def payment(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    shopping_cart: ShoppingCart = data['ShoppingCart']
    if shopping_cart.price < LIMIT_PRICE:
        await message.answer(f"Сумма минимального заказа {LIMIT_PRICE} USDT. "
                             f"Стоимость покупки изменена до минимальной стоимости",
                             show_alert=True)
        shopping_cart.price = LIMIT_PRICE
        await state.update_data(ShoppingCart=shopping_cart)

    shopping_cart = await create_deal(state=state, user_id=id, message_id=message.message.message_id)
    client_transaction_id = f"{shopping_cart.deal_id}-{id}-{shopping_cart.price}-{datetime.now().timestamp()}"
    order: CreatedOrder = await ExNode.create_order(client_transaction_id=client_transaction_id,
                                                    amount=float(shopping_cart.price),
                                                    merchant_uuid=MERCHANT_ID)

    shopping_cart.tracker_id = order.tracker_id
    if order.date_expire:
        date_expire = format_date(order.date_expire)
        await bot.edit_message_text(chat_id=id,
                                    message_id=message.message.message_id,
                                    text=get_mes("receiver", price=shopping_cart.price, receiver=order.receiver,
                                                 date_expire=date_expire),
                                    parse_mode=ParseMode.MARKDOWN_V2,
                                    reply_markup=await Keyboards.payment()
                                    )
    else:
        await bot.edit_message_text(chat_id=id,
                                    message_id=message.message.message_id,
                                    text=get_mes("receiver", price=shopping_cart.price, receiver=order.receiver),
                                    parse_mode=ParseMode.MARKDOWN_V2,
                                    reply_markup=await Keyboards.payment()
                                    )

    await state.update_data(ShoppingCart=shopping_cart)


@router.callback_query(UserStates.ShoppingCart, F.data == "complete_payment")
async def complete_payment(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    shopping_cart: ShoppingCart = data['ShoppingCart']
    received_order: ReceivedOrder = await ExNode.get_order(tracker_id=shopping_cart.tracker_id)
    if received_order.status == "SUCCESS":
        data = ""
        count = 1
        for account_id in shopping_cart.accounts_id:
            account = await accounts.get(account_id)
            data += f"{count}) {account.data}\n\n"

        seller = await sellers.get()
        await bot.edit_message_text(chat_id=id,
                                    message_id=message.message.message_id,
                                    text=data,
                                    reply_markup=Keyboards.support_kb)
        deals_id = [str(shopping_cart.deal_id)]
        account = await accounts.get(shopping_cart.accounts_id[0])
        if shopping_cart.guarantor is False:
            text = get_mes("mark_seller")
            keyboard = Keyboards.mark_seller_kb
            seller.balance += account.price * shopping_cart.count
            guarantor = "без гаранта"
        else:
            text = get_mes("support_24_hours")
            keyboard = await Keyboards.confirm_account_user_kb(deals_id)
            guarantor = "с гарантом"

        await bot.send_message(chat_id=seller.id,
                               text=get_mes("complete_payment",
                                            user_id=id,
                                            deal_id=", ".join(deals_id),
                                            amount=rounding_numbers(str(account.price * shopping_cart.count)),
                                            guarantor=guarantor)
                               )

        for deals_id in shopping_cart.deals_id:
            deal = await deals.get(deals_id)
            if shopping_cart.guarantor is False:
                deal.payment_status = 2
            else:
                deal.payment_status = 1
            await deals.update(deal)
        await bot.send_message(chat_id=id,
                               text=text,
                               reply_markup=keyboard)
    else:
        await message.answer("Счет ещё не оплачен! Не уходите с этого этапа")

