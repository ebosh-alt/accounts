from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from data.config import link_support


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
    
    @staticmethod
    def create_force_reply(text: str):
        return types.ForceReply(input_field_placeholder=text)


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
        "Просмотреть инфо продавца": "show_seller_info"}
        )
    admin_back_menu_kb = Builder.create_keyboard({"Назад": "admin_back_menu"})
    manager_menu_kb = Builder.create_keyboard(
        {
            "Выставить счет": "create_deal",
            "Загрузить аккаунты": "load_accs"
        }
    )
    manager_back_menu_kb = Builder.create_keyboard({"Назад": "manager_back_menu"})

    # def manager_create_deal_input_filed_guarant(text:str) :
    #     return Builder.create_force_reply(text=text)

    manager_deal_cr_choose_g_type = Builder.create_keyboard(
        {
            "С гарантом": "cr_deal_g",
            "Без гаранта": "cr_deal_not_g"
        }
    )
    
    manager_deal_cr_confirm = Builder.create_keyboard(
        {
            "Подтвердить": "cr_deal_success",
            "Отмена": "cr_deal_unsuccess"
        }
    )

    confirm_cr_deal_by_user = Builder.create_keyboard(
        {
            "Оплатить": "confirm_cr_deal_user",
        }
    )
    
