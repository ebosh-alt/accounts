import logging
from config.config import config

from service.TGClient import TG_Acc, TGClient_S

from aiogram import Dispatcher, Bot


logger = logging.getLogger(__name__)

dp = Dispatcher()
bot = Bot(config.telegram_bot.token)
tg_acc = TG_Acc(session_name=config.telegram_client.session_path, api_id=config.telegram_client.api_id, api_hash=config.telegram_client.api_hash, phone_number=config.telegram_client.phone_number)
client_s = TGClient_S(tg_acc)

    

