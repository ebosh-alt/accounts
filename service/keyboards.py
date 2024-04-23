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
    admin_kb = Builder.create_keyboard(
        {"Отменить покупку": "cancel_buy",
         "Просмотреть сделки": "show_deals",
         "Просмотреть инфо продавца": "show_seller_info"}
    )

    @staticmethod
    async def shops_kb():
        shops = await accounts.get_shops()
        shops.append("В главное меню")
        logger.info(f"{shops}")
        kb = Builder.create_keyboard(shops)
        return kb

    @staticmethod
    async def name_accounts_shop_kb(shop):
        names = await accounts.get_name_accounts_shop(shop)
        names.append("В главное меню")
        logger.info(f"{names}")
        kb = Builder.create_keyboard(names)
        return kb

    @staticmethod
    async def confirm_basket(id_account: int):
