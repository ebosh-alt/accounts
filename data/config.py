import logging

from aiogram import Dispatcher, Bot

from data.settings.setting import Config
from service.TGClient import TG_Acc, TGClient_S

logger = logging.getLogger(__name__)

config = Config.load()
logger.info(config.db)
logger.info(config.admin)
# dp = Dispatcher()
# bot = Bot(bot_token)
#
# tg_acc = TG_Acc(session_name=session_path, api_id=api_id, api_hash=api_hash, phone_number=phone_number)
# client_s = TGClient_S(tg_acc)
#
