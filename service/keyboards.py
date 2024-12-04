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
    def create_reply_keyboard(name_buttons: list = None, one_time_keyboard: bool = False, request_contact: bool = False,
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
        {"🛒 Перейти в магазин аккаунтов": "shop",
         "📜 Прочитать правила": "rules",
         "🛠 Написать в поддержку": link_support,
         "📦 Посмотреть историю покупок": "history_buy"})
    back_menu_kb = Builder.create_keyboard({"Назад": "back_menu"})

    admin_menu_kb = Builder.create_keyboard(
        {"Отменить покупку": "cancel_buy",
         "Просмотреть сделки": "show_deals",
         "Просмотреть инфо продавца": "show_seller_info",
         "Изменить баланс": "change_balance",
         "Изменить реквизиты продавца": "change_seller_wallet",
         "Изменить название магазина": "change_name_shop",
         "Изменить описание продавца": "change_description_seller",
         "Добавить тип аккаунтов": "add_acc_type",
         "Удалить тип аккаунтов": "delete_acc_type",
         })

    admin_back_menu_kb = Builder.create_keyboard({"Назад": "admin_back_menu"})

    manager_menu_kb = Builder.create_keyboard(
        {
            "Изменить каталог": "load_accs",
            "Выставить счет": "create_deal",
            "Изменить реквизиты": "change_wallet",
            "Изменить название магазина": "change_name_shop",
            "Изменить описание продавца": "change_description_seller",
        }
    )
    manager_menu_load_kb = Builder.create_keyboard(
        {
            "Загрузить ещё аккаунты": "load_accs",
            "Выставить счет": "create_deal",
            "Изменить название магазина": "change_name_shop",
            "Изменить описание продавца": "change_description_seller",
        }
    )

    manager_loads_accs_tree_kb = Builder.create_keyboard(
        {
            "Заменить каталог": "new_catalog",
            "Изменить каталог": "change_catalog",
            "Удалить из каталога": "delete_from_catalog",
            "Назад": "manager_back_menu",
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

    # choice_count_account_kb

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

    def freeze_deal_kb(deal_id: int):
        keyboard = Builder.create_keyboard({
            "Заморозить сделку": f"admin_freeze_deal_{deal_id}",
        })
        return keyboard

    def descision_deal_freezing(deal_id: int):
        keyboard = Builder.create_keyboard({
            "Подтвердить сделку": f"confirm_freezed_deal_{deal_id}",
            "Отменить сделку": f"cancel_freezed_deal_{deal_id}",
        })
        return keyboard

    confirm_payment_kb = Builder.create_keyboard({
        "В главное меню": "В главное меню",
        "Поддержка": link_support})

    mark_seller_kb = Builder.create_keyboard({
        "0": "0",
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
    })

    @staticmethod
    async def confirm_account_user_kb(deals_id):
        deals_id = [str(id) for id in deals_id]
        return Builder.create_keyboard({
            "Ок": f"ok_account_{','.join(deals_id)}",
            "Не ок": f"defect_account_{','.join(deals_id)}",
            "Написать в поддержку": link_support

        })

    @staticmethod
    async def choice_action():
        # buttons = await accounts.get_shops()
        buttons = ["Перейти к выбору категорий", "Общение с продавцом", "Вернуться в главное меню"]
        kb = Builder.create_keyboard(buttons)
        return kb

    @staticmethod
    async def shop_kb():
        buttons = await accounts.get_shops()
        buttons.append("Вернуться к выбору действия")
        buttons.append("Вернуться в главное меню")
        kb = Builder.create_keyboard(buttons)
        return kb

    @staticmethod
    async def choice_action_name_account():
        # buttons = await accounts.get_name_accounts_shop(shop)
        buttons = ["Перейти к выбору товаров", "Написать продавцу", "Вернуться в главное меню"]
        kb = Builder.create_keyboard(buttons)
        return kb

    @staticmethod
    async def name_accounts_shop_kb(shop):
        buttons = await accounts.get_name_accounts_shop(shop)
        buttons.append("Вернуться к выбору действия")
        buttons.append("Вернуться в главное меню")
        # buttons.append("Вернуться к выбору магазина")
        # buttons.append("В главное меню")
        logger.info(f"{buttons}")
        kb = Builder.create_keyboard(buttons)
        return kb

    @staticmethod
    async def payment_manually(deal_id):
        confirm_cr_deal_by_user = Builder.create_keyboard(
            {
                "Оплатить": f"payment_manually_{deal_id}",
            }
        )
        return confirm_cr_deal_by_user

    @staticmethod
    async def payment(link: str = None):
        return Builder.create_keyboard({
            "Оплатил": "complete_payment"
        })

    @staticmethod
    async def choice_count_account(count: int = None):
        if count <= 1:
            return Builder.create_keyboard({
                "C гарантом": f"yes_guarantor",
                "Без гаранта": f"no_guarantor",
                "Вернуться к выбору товаров": "Вернуться к выбору товаров",
                "В главное меню": "В главное меню"
            })
        else:
            return Builder.create_keyboard({
                "-1": "remove_account",
                "+1": "add_account",
                "C гарантом": f"yes_guarantor",
                "Без гаранта": f"no_guarantor",
                "Вернуться к выбору товаров": "Вернуться к выбору товаров",
                "В главное меню": "В главное меню"
            }, 2, 2, 1, 1)
