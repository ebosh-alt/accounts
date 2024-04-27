from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from data.config import bot
from models.models import DataDeals
from service.GetMessage import get_mes


async def send(message: CallbackQuery, all_data_deals: list[DataDeals], fmes_text_path: str, keyboard):
    """service.GetMessage.get_mes() использует в качестве аргумента fmes_text_path\n
    fmes_text_path - название файла .md\n
    get_mes(fmes_text_path)"""
    ind = 0
    new_data = list()
    count_symbol = 0
    while ind < len(all_data_deals):
        count_symbol += all_data_deals[ind].len() + 130
        if count_symbol < 2000:
            new_data.append(all_data_deals[ind])
        else:
            await bot.send_message(
                chat_id=message.message.chat.id,
                text=get_mes("history_buy_user", deals=new_data),
                parse_mode=ParseMode.MARKDOWN_V2
            )
            count_symbol = 0
            new_data = list()
            new_data.append(all_data_deals[ind])
        ind += 1
    if len(new_data) != 0:
        await bot.send_message(
            chat_id=message.message.chat.id,
            text=get_mes("history_buy_user", deals=new_data),
            parse_mode=ParseMode.MARKDOWN_V2
        )
    await bot.send_message(
        chat_id=message.message.chat.id,
        text=get_mes(fmes_text_path),
        reply_markup=keyboard
    )
