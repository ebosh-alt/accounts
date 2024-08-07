import logging

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from data.config import bot, CryptoCloud, BASE_PERCENT, PERCENT_GUARANTOR
from filters.Filters import IsShop, IsNameAccount
from models.StateModels import ShoppingCart
from models.database import deals, accounts, sellers
from service.GetMessage import get_mes, rounding_numbers
from service.buy_automatically import set_data_shopping_cart, create_deal
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
    await state.set_state(UserStates.ShoppingCart)


@router.callback_query(F.data == "Перейти к выбору категорий", UserStates.ShoppingCart)
async def choose_shop(message: CallbackQuery):
    id = message.from_user.id
    # await message.message.delete()
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("shop_user_categories"),
                                reply_markup=await Keyboards.shop_kb())


@router.callback_query(IsShop(), UserStates.ShoppingCart)
async def choose_after_shop_act(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    await set_data_shopping_cart(state=state, message=message.data)
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("shop_user"),
                                reply_markup=await Keyboards.choice_action_name_account())


@router.callback_query(F.data.in_(("Перейти к выбору товаров", "Вернуться к выбору товаров")), UserStates.ShoppingCart)
async def choice_account(message: CallbackQuery, state: FSMContext):
    # выбор аккаунта и сохранение выбранного магазина
    id = message.from_user.id
    # shopping_cart = await set_data_shopping_cart(state=state, message=message.data)
    data = await state.get_data()
    shopping_cart = data["ShoppingCart"]
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text="Выберите товар",
                                reply_markup=await Keyboards.name_accounts_shop_kb(shop=shopping_cart.shop))


@router.callback_query(UserStates.ShoppingCart, IsNameAccount())
async def choice_guarantor(message: CallbackQuery, state: FSMContext):
    # сохранение имени выбранного аккаунта и выбор количества аккаунтов
    shopping_cart: ShoppingCart
    count_account: int
    id = message.from_user.id
    shopping_cart, count_account = await set_data_shopping_cart(state, name=message.data)
    # account_id = shopping_cart.accounts_id[0]
    # account = await accounts.get(account_id)
    price_no = rounding_numbers("%.2f" % (shopping_cart.price * (1 + BASE_PERCENT / 100) * shopping_cart.count))
    price_yes = rounding_numbers("%.2f" % (shopping_cart.price * (1 + PERCENT_GUARANTOR / 100) * shopping_cart.count))
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("shopping_cart_user",
                                             shop=shopping_cart.shop,
                                             name=shopping_cart.name,
                                             price_no=price_no,
                                             price_yes=price_yes,
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
    price_no = rounding_numbers("%.2f" % (shopping_cart.price * (1 + BASE_PERCENT / 100) * shopping_cart.count))
    price_yes = rounding_numbers("%.2f" % (shopping_cart.price * (1 + PERCENT_GUARANTOR / 100) * shopping_cart.count))

    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("shopping_cart_user",
                                             shop=shopping_cart.shop,
                                             name=shopping_cart.name,
                                             price_no=price_no,
                                             price_yes=price_yes,
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
                                             price=rounding_numbers(str(shopping_cart.price)),
                                             description=shopping_cart.description,
                                             choice_count=shopping_cart.count
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
                                text=f"Ниже лежит счет — проведите оплату по нему и нажмите кнопку «Оплачено»\n\nСчет на оплату: {link}",
                                reply_markup=await Keyboards.payment(link))
    await state.update_data(ShoppingCart=shopping_cart)
    await create_deal(state=state, user_id=id, message_id=message.message.message_id)


@router.callback_query(UserStates.ShoppingCart, F.data == "complete_payment")
async def complete_payment(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    shopping_cart: ShoppingCart = data['ShoppingCart']
    invoice = CryptoCloud.get_invoice_info([shopping_cart.uuid])
    if invoice["result"][0]["status"] == "paid" or True:
        # if invoice["result"][0]["status"] == "paid" or invoice["result"][0]["status"] == True:
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
        deals_id = [str(id) for id in shopping_cart.deals_id]
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

