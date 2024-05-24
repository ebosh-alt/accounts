import logging

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from data.config import bot, PERCENT, CryptoCloud, BASE_PERCENT
from filters.Filters import IsShop, IsNameAccount
from models.StateModels import ShoppingCart
from models.database import deals, accounts, sellers, Account
from service.GetMessage import get_mes
from service.buy_automatically import set_data_shopping_cart, create_deal
from service.keyboards import Keyboards
from states.states import UserStates

logger = logging.getLogger(__name__)
router = Router()

buy_automatically_rt = router


@router.callback_query((F.data == "shop") | (F.data == "Вернуться к выбору магазина"))
async def menu_shop(message: CallbackQuery, state: FSMContext):
    # главное меню покупки аккаунтов и выбор магазина
    id = message.from_user.id
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("shop_user"),
                                reply_markup=await Keyboards.shops_kb())
    await state.set_state(UserStates.ShoppingCart)


@router.callback_query(IsShop(), UserStates.ShoppingCart)
async def choice_account(message: CallbackQuery, state: FSMContext):
    # выбор аккаунта и сохранение выбранного магазина
    id = message.from_user.id
    shopping_cart = await set_data_shopping_cart(state=state, message=message.data)
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text="Выберите аккаунт",
                                reply_markup=await Keyboards.name_accounts_shop_kb(shop=shopping_cart.shop))


@router.callback_query(UserStates.ShoppingCart, IsNameAccount())
async def choice_guarantor(message: CallbackQuery, state: FSMContext):
    # сохранение имени выбранного аккаунта и выбор количества аккаунтов
    shopping_cart: ShoppingCart
    count_account: int
    id = message.from_user.id
    shopping_cart, count_account = await set_data_shopping_cart(state, name=message.data)
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("shopping_cart_user",
                                             shop=shopping_cart.shop,
                                             name=shopping_cart.name,
                                             price_no=shopping_cart.price * shopping_cart.count,
                                             price_yes=float("%.2f" % (shopping_cart.price * (
                                                     1 + PERCENT / 100))) * shopping_cart.count,
                                             description=shopping_cart.description,
                                             count=count_account,
                                             choice_count=shopping_cart.count
                                             ),
                                parse_mode=ParseMode.MARKDOWN_V2,
                                reply_markup=await Keyboards.choice_count_account(count=count_account))


@router.callback_query(UserStates.ShoppingCart, F.data.in_(["add_account", "remove_account"]))
async def choice_count_account(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    shopping_cart: ShoppingCart = data['ShoppingCart']
    count_account = len(await accounts.get_account_by_name(name=shopping_cart.name, shop=shopping_cart.shop))
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
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("shopping_cart_user",
                                             shop=shopping_cart.shop,
                                             name=shopping_cart.name,
                                             price_no=shopping_cart.price * shopping_cart.count,
                                             price_yes=float("%.2f" % (shopping_cart.price * (
                                                     1 + PERCENT / 100))) * shopping_cart.count,
                                             description=shopping_cart.description,
                                             count=count_account,
                                             choice_count=shopping_cart.count
                                             ),
                                parse_mode=ParseMode.MARKDOWN_V2,
                                reply_markup=await Keyboards.choice_count_account(count=count_account))


@router.callback_query(UserStates.ShoppingCart, F.data.contains("guarantor"))
async def confirm_shopping_cart(message: CallbackQuery, state: FSMContext):
    # переход к оплате или отмена и сохранение с или без гаранта
    id = message.from_user.id
    shopping_cart = await set_data_shopping_cart(state, guarantor=message.data)
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("shopping_cart_user",
                                             shop=shopping_cart.shop,
                                             name=shopping_cart.name,
                                             price=shopping_cart.price,
                                             description=shopping_cart.description
                                             ),
                                parse_mode=ParseMode.MARKDOWN_V2,
                                reply_markup=Keyboards.ready_payment_kb)


@router.callback_query(UserStates.ShoppingCart, F.data == "payment")
async def payment(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    shopping_cart: ShoppingCart = data['ShoppingCart']
    invoice = CryptoCloud.create_invoice(amount=shopping_cart.price)
    shopping_cart.uuid = invoice["result"]["uuid"]
    link = invoice["result"]["link"]
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text="здесь будет счет на оплату",
                                reply_markup=await Keyboards.payment(link))
    await state.update_data(ShoppingCart=shopping_cart)
    await create_deal(state=state, user_id=id, message_id=message.message.message_id)


@router.callback_query(UserStates.ShoppingCart, F.data == "complete_payment")
async def complete_payment(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    shopping_cart: ShoppingCart = data['ShoppingCart']
    invoice = CryptoCloud.get_invoice_info([shopping_cart.uuid])
    if invoice["result"][0]["status"] == "paid":
        data = ""
        for account_id in shopping_cart.accounts_id:
            account = await accounts.get(account_id)
            data += account.data + "\n\n"
        seller = await sellers.get()
        await bot.edit_message_text(chat_id=id,
                                    message_id=message.message.message_id,
                                    text=data,
                                    reply_markup=Keyboards.support_kb)

        if shopping_cart.guarantor is False:
            text = get_mes("mark_seller")
            keyboard = Keyboards.mark_seller_kb
            seller.balance += float("%.2f" % (shopping_cart.price * (1 - BASE_PERCENT / 100)))
        else:
            text = get_mes("support_24_hours")
            keyboard = Keyboards.confirm_account_user_kb

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


@router.callback_query(UserStates.ShoppingCart, F.data == "ok_account")
async def complete_payment(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    shopping_cart: ShoppingCart = data['ShoppingCart']
    for deal_id in shopping_cart.deals_id:
        deal = await deals.get(deal_id)
        deal.payment_status = 2
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
