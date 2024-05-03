from typing import Callable, TypeVar, Any

from adaptix import Retort
from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from environs import Env

# from models.database.accounts import Accounts
from service.TGClient import TG_Acc, TGClient_S

env = Env()
env.read_env()

bot_token = env('BOT_TOKEN')
# BOT_ID = bot_token.split(":")[0]
link_support = env('LINK_SUPPORT')

dp = Dispatcher()
bot = Bot(bot_token)
BOT_ID = bot.id
print(BOT_ID)
link_to_bot = "https://t.me/selling_accounts_test_bot"

session_path = env('SESSION_PATH')
api_id = int(env('API_ID'))
api_hash = env('API_HASH')
phone_number = env('PHONE_NUMBER')
SQLALCHEMY_DATABASE_URI = f'sqlite+aiosqlite:///data/database.db'

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

ADMINS = [int(admin_id) for admin_id in env('ADMINS').split()]

SELLER = int(env('SELLER'))

PERCENT = float(env('PERCENT'))
EXCEL_TEMPLATE_PATH = env('EXCEL_TEMPLATE_PATH')
EXCEL_LOAD_FILE_PATH = env('EXCEL_LOAD_FILE_PATH')
USERNAME = env("USERNAME")
