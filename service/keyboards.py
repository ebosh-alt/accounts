from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


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


start_menu_admin_kb = create_keyboard(["Редактирование предстартового сообщения"])

edit_before_start_message_button = ["Изменить видимость", "Медиа", "Клавиатура"]
edit_before_start_message_kb = create_keyboard(edit_before_start_message_button)


