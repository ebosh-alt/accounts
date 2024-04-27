import logging

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from data.config import link_support
from models.database import accounts

logger = logging.getLogger(__name__)


class Builder:
    @staticmethod
    def create_keyboard(name_buttons: list | dict, *sizes: int) -> types.InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        if type(name_buttons) is list:
            for name_button in name_buttons:
                keyboard.button(
                    text=name_button, callback_data=name_button
                )
        elif type(name_buttons) is dict:
            for name_button in name_buttons:
                if "http" in name_buttons[name_button] or "@" in name_buttons[name_button]:
                    keyboard.button(
                        text=name_button, url=name_buttons[name_button]
                    )
                else:
                    keyboard.button(
                        text=name_button, callback_data=name_buttons[name_button]
                    )

        if len(sizes) == 0:
            sizes = (1,)
        keyboard.adjust(*sizes)
        return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True)

    @staticmethod
    def create_reply_keyboard(name_buttons: list, one_time_keyboard: bool = False, request_contact: bool = False,
                              *sizes) -> types.ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardBuilder()
        for name_button in name_buttons:
            if name_button is not tuple:
                keyboard.button(
                    text=name_button,
                    request_contact=request_contact
                )
            else:
                keyboard.button(
                    text=name_button,
                    request_contact=request_contact

                )
        if len(sizes) == 0:
            sizes = (1,)
        keyboard.adjust(*sizes)
        return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=one_time_keyboard)


class Keyboards:
    menu_kb = Builder.create_keyboard(
        {"Магазин": "shop",
         "Правила": "rules",
         "Поддержка": link_support,
         "История покупок": "history_buy"})
    back_menu_kb = Builder.create_keyboard({"Назад": "back_menu"})
    admin_menu_kb = Builder.create_keyboard(
        {"Отменить покупку": "cancel_buy",
         "Просмотреть сделки": "show_deals",
         "Просмотреть инфо продавца": "show_seller_info"
        })
    admin_back_menu_kb = Builder.create_keyboard({"Назад": "admin_back_menu"})

    choice_guarantor_kb = Builder.create_keyboard({
        "C гарантом": f"yes_guarantor",
        "Без гаранта": f"no_guarantor",
        "Вернуться к выбору аккаунта": "back_to_choice_account",
        "В главное меню": "В главное меню"
    })
    ready_payment_kb = Builder.create_keyboard({
        "Оплата": "payment",
        "Вернуться к выбору аккаунта": "back_to_choice_account",
        "В главное меню": "В главное меню"
    })

    payment_kb = Builder.create_keyboard({
        "Оплатил": "complete_payment"
    })
    support_kb = Builder.create_keyboard({
        "Поддержка": link_support
    })
    confirm_payment_kb = Builder.create_keyboard({
        "В главное меню": "В главное меню",
        "Поддержка": link_support})

    mark_seller_kb = Builder.create_keyboard({
        "0": "0",
        "1": "1"
    })
    confirm_account_user_kb = Builder.create_keyboard({
        "Ок": "ok_account"
    })

    @staticmethod
    async def shops_kb():
        buttons = await accounts.get_shops()
        buttons.append("Общение с продавцом")
        buttons.append("В главное меню")
        logger.info(f"{buttons}")
        kb = Builder.create_keyboard(buttons)
        return kb

    @staticmethod
    async def name_accounts_shop_kb(shop):
        buttons = await accounts.get_name_accounts_shop(shop)
        buttons.append("Вернуться к выбору магазина")
        buttons.append("В главное меню")
        logger.info(f"{buttons}")
        kb = Builder.create_keyboard(buttons)
        return kb


    
