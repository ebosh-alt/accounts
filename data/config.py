from typing import Callable, TypeVar, Any

from adaptix import Retort
from aiogram import Dispatcher, Bot
from environs import Env
from service.TGClient import TG_Acc, TGClient_S

env = Env()
env.read_env()

bot_token = env('BOT_TOKEN')
link_support = env('LINK_SUPPORT')
dp = Dispatcher()
bot = Bot(bot_token, parse_mode="Markdown")

link_to_bot = "https://t.me/selling_accounts_test_bot"

session_path = env('SESSION_PATH')
api_id = int(env('API_ID'))
api_hash = env('API_HASH')
phone_number = env('PHONE_NUMBER')
tg_acc = TG_Acc(session_name=session_path, api_id=api_id, api_hash=api_hash, phone_number=phone_number)
client_s = TGClient_S(tg_acc)

API_BASE_URL = "https://api.cryptomus.com/{}"
DEFAULT_TIMEOUT = 60.0
DEFAULT_HEADERS = {
    "merchant": "",
    "sign": "",
    "Content-Type": "application/json"
}
ResponseType = TypeVar("ResponseType")
JsonDumps = Callable[..., Any]
retort = Retort()
cryptomus_merchant_id = env('MERCHANT_ID')
cryptomus_api_key = env('API_KEY')
