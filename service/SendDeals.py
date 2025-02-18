from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from internal.app.app import bot
from internal.entities.models import DataDeals
from service.GetMessage import get_mes, rounding_numbers


async def send(message: CallbackQuery, all_data_deals: list[DataDeals], keyboard):
    """service.GetMessage.get_mes() использует в качестве аргумента fmes_text_path\n
    fmes_text_path - название файла .md\n
    get_mes(fmes_text_path)"""
    ind = 0
    new_data = list()
    count_symbol = 0
    if len(all_data_deals) == 0:
        await message.answer("У вас ещё нет совершенных сделок")
        return
    while ind < len(all_data_deals):

        data_deal = all_data_deals[ind]
        ind += 1
        count_symbol += data_deal.len() + 130
        data_deal.price = rounding_numbers(str(data_deal.price))
        if count_symbol < 2000:
            new_data.append(data_deal)
        else:
            await bot.send_message(
                chat_id=message.message.chat.id,
                text=get_mes("history_buy", deals=new_data),
                parse_mode=ParseMode.MARKDOWN_V2
            )
            count_symbol = 0
            new_data = list()
            new_data.append(data_deal)

    if len(new_data) != 0:
        await bot.send_message(
            chat_id=message.message.chat.id,
            text=get_mes("history_buy", deals=new_data),
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=keyboard
        )

