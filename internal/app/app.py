import logging
from config.config import config

from service.TGClient import TG_Acc, TGClient_S

from aiogram import Dispatcher, Bot


logger = logging.getLogger(__name__)

dp = Dispatcher() # https://github.com/ebosh-alt/accounts/pull/10/conflict?name=internal%252Fapp%252Fapp.py&ancestor_oid=8ad15347c69d5f85341267954766e29cb4a50476&base_oid=a6b5028c0ca8603e15df5bded9dd6e9dcef013d0&head_oid=fab21076a7e0d9eaab9eb8b18244f414dcef83c6
bot = Bot(config.telegram_bot.token)
tg_acc = TG_Acc(session_name=config.telegram_client.session_path, api_id=config.telegram_client.api_id, api_hash=config.telegram_client.api_hash, phone_number=config.telegram_client.phone_number)
client_s = TGClient_S(tg_acc)

