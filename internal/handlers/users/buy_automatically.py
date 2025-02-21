import logging
from datetime import datetime

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config.config import config


from internal.app.app import bot
from internal.filters.Filters import IsCategory, IsSubcategory, IsNameAccount
from internal.entities.states.StateModels import ShoppingCart, AccountMD
from internal.entities.database import deals, accounts, sellers, categories
from internal.entities.models import CreatedOrder, ReceivedOrder
from service import cryptography
from service.GetMessage import get_mes, rounding_numbers
from service.buy_automatically import set_data_shopping_cart, create_deal
from service.date import format_date
from service.exnode import ExNode
from service.keyboards import Keyboards
from internal.entities.states.states import UserStates

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
async def choose_category(message: CallbackQuery):
    id = message.from_user.id
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("shop_user_categories"),
                                reply_markup=await Keyboards.categories_kb())


@router.callback_query(IsCategory(), UserStates.ShoppingCart)
async def choose_after_category_act(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id

    # await set_data_shopping_cart(state=state, category=message.data)
    shopping_cart: ShoppingCart = ShoppingCart(category=message.data)
    await state.update_data(ShoppingCart=shopping_cart)
    logger.info(f"Shopping Cart: {shopping_cart}")
    
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("shop_user"),
                                reply_markup=await Keyboards.choice_action_subcategories_account())


@router.callback_query(F.data.in_(("Перейти к выбору подкатегорий", "Вернуться к выбору подкатегорий")), UserStates.ShoppingCart)
async def choose_subcategory(message: CallbackQuery, state: FSMContext):
    # выбор аккаунта и сохранение выбранного магазина
    id = message.from_user.id
    data = await state.get_data()
    shopping_cart: ShoppingCart = data['ShoppingCart']
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text="Выберите подкатегорию",
                                reply_markup=await Keyboards.subcategories_kb(category=shopping_cart.category))
    

@router.callback_query(IsSubcategory(), UserStates.ShoppingCart)
async def choose_after_subcategory_act(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id

    data = await state.get_data()
    shopping_cart: ShoppingCart = data['ShoppingCart']
    shopping_cart.subcategory = message.data
    await state.update_data(ShoppingCart=shopping_cart)
    logger.info(f"Shopping Cart: {shopping_cart}")
    # await set_data_shopping_cart(state=state, category=message.data, subcategory)
    
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("shop_user"),
                                reply_markup=await Keyboards.choice_action_name_account())


@router.callback_query(F.data.in_(("Перейти к выбору товаров", "Вернуться к выбору товаров", "<", ">")), UserStates.ShoppingCart)
async def choice_account(message: CallbackQuery, state: FSMContext):
    # выбор аккаунта и сохранение выбранного магазина
    id = message.from_user.id
    
    data = await state.get_data()
    shopping_cart: ShoppingCart = data['ShoppingCart']
    if "slider_page" in data:
        slider_page = data["slider_page"]
    else:
        slider_page = 0
    
    acc_names_not_unique, accs = await categories.get_viewed_accs_by_category_subcategory(category=shopping_cart.category, subcategory=shopping_cart.subcategory)
    len_accs = len(accs)
    
    if message.data == "Перейти к выбору товаров":
        slider_page = 0
    elif message.data == "<":
        if slider_page - 5 < 0:
            slider_page = len_accs - 5
        else:
            slider_page = (slider_page - 5) % len_accs
    elif message.data == ">":
        if slider_page + 5 >= len_accs:
            slider_page = 0
        else:
            slider_page = (slider_page + 5) % len_accs
    await state.update_data(slider_page=slider_page)
    
    acc_names = []
    for acc_n_u in acc_names_not_unique:
        if acc_n_u not in acc_names:
            acc_names.append(acc_n_u)
            
    accs_for_text = []
    logger.info(slider_page)
    for i in range(slider_page, slider_page+5):
        if i>=len_accs:
            break
        acc_md = AccountMD(
            category=shopping_cart.category, 
            subcategory=shopping_cart.subcategory,
            name=acc_names[i],
            description=accs[i].description,
            price_no=rounding_numbers("%.2f" % (accs[i].price * (1 + config.shop.base_percent / 100))),
            price_yes=rounding_numbers("%.2f" % (accs[i].price * (1 + config.shop.percent_guarantor / 100))),
            link=f"{config.telegram_bot.link}?start={cryptography.encode(shopping_cart.category + '%' + shopping_cart.subcategory + '%' + acc_names[i])}"
            )
        accs_for_text.append(acc_md)

    text=get_mes(
        "accs_urls",
        screening=False,
        accs=accs_for_text,
    )
    logger.info(shopping_cart)
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=text,
                                reply_markup=Keyboards.name_accounts_slider_kb(),
                                parse_mode=ParseMode.MARKDOWN_V2
                                )


# @router.callback_query(UserStates.ShoppingCart)
async def choice_guarantor(message: CallbackQuery | Message, state: FSMContext, category: str = None, subcategory: str = None, name: str = None):
    # сохранение имени выбранного аккаунта и выбор количества аккаунтов
    shopping_cart: ShoppingCart
    count_account: int
    id = message.from_user.id
    
    logger.info(f"{category}, {name}")
    if name is None:
        name = message.data
        print(message.data)

    shopping_cart, count_account, acc = await set_data_shopping_cart(state, name=name, category=category, subcategory=subcategory)
    await state.set_state(UserStates.ShoppingCart)
    price_no = rounding_numbers("%.2f" % (acc.price * (1 + config.shop.base_percent / 100) * shopping_cart.count))
    price_yes = rounding_numbers("%.2f" % (acc.price * (1 + config.shop.percent_guarantor / 100) * shopping_cart.count))
    
    link = f"{config.telegram_bot.link}?start={cryptography.encode(shopping_cart.category + '%' + shopping_cart.subcategory + '%' + shopping_cart.name)}"
    
    reply_markup = await Keyboards.choice_count_account(count=count_account)
    
    text = get_mes("shopping_cart_user",
                   category=shopping_cart.category,
                   subcategory=shopping_cart.subcategory,
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
    accs = await categories.get_viewed_accs_by_category_subcategory_acc(shopping_cart.category, shopping_cart.subcategory, shopping_cart.name)
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
    price_no = rounding_numbers("%.2f" % (accs[0].price * (1 + config.shop.base_percent / 100) * shopping_cart.count))
    price_yes = rounding_numbers("%.2f" % (accs[0].price * (1 + config.shop.percent_guarantor / 100) * shopping_cart.count))
    link = f"{config.telegram_bot.link}?start={cryptography.encode(shopping_cart.shop + '%' + shopping_cart.name)}"
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("shopping_cart_user",
                                             category=shopping_cart.category,
                                             subcategory=shopping_cart.subcategory,
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
    data = await state.get_data()
    logger.info(data.get("ShoppingCart"))
    shopping_cart: ShoppingCart = await set_data_shopping_cart(state, guarantor=message.data)

    link = f"{config.telegram_bot.link}?start={cryptography.encode(shopping_cart.category + '%' + shopping_cart.subcategory + '%' + shopping_cart.name)}"
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("shopping_cart_user",
                                             category=shopping_cart.category,
                                             subcategory=shopping_cart.subcategory,
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
    if shopping_cart.price < config.shop.limit_price:
        await message.answer(f"Сумма минимального заказа {config.shop.limit_price} USDT. "
                             f"Стоимость покупки изменена до минимальной стоимости",
                             show_alert=True)
        shopping_cart.price = config.shop.limit_price
        await state.update_data(ShoppingCart=shopping_cart)

    shopping_cart = await create_deal(state=state, user_id=id, message_id=message.message.message_id)
    client_transaction_id = f"{shopping_cart.deal_id}-{id}-{shopping_cart.price}-{datetime.now().timestamp()}"
    order: CreatedOrder = await ExNode.create_order(client_transaction_id=client_transaction_id,
                                                    amount=float(shopping_cart.price),
                                                    merchant_uuid=config.exnode.merchant_id)

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
    logger.info(shopping_cart)
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
                                    reply_markup=Keyboards.support_kb,
                                    parse_mode=None)
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

        deal = await deals.get(shopping_cart.deal_id)
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

