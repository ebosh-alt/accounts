from typing import Callable, TypeVar, Any

from aiogram import Dispatcher, Bot
from environs import Env

from service.TGClient import TG_Acc, TGClient_S
from service.exnode import ExNodeClient

env = Env()
env.read_env()

bot_token = env('BOT_TOKEN')
link_support = env('LINK_SUPPORT')

dp = Dispatcher()
bot = Bot(bot_token)
BOT_ID = bot.id
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

ADMINS = [int(admin_id) for admin_id in env('ADMINS').split()]
MAIN_ADMIN = int(env('MAIN_ADMIN'))

SELLER = int(env('SELLER'))
BASE_PERCENT = float(env("BASE_PERCENT"))
PERCENT_GUARANTOR = float(env('PERCENT_GUARANTOR'))
EXCEL_TEMPLATE_PATH = env('EXCEL_TEMPLATE_PATH')
EXCEL_LOAD_FILE_PATH = env('EXCEL_LOAD_FILE_PATH')
USERNAME = env("USERNAME")
# CRYPTO_API = env("CRYPTO_API")
# CRYPTO_SHOP_ID = env("CRYPTO_SHOP_ID")
# CryptoCloud: CryptoCloudClient = CryptoCloudClient(CRYPTO_API, CRYPTO_SHOP_ID)
EXNODE_PUBLIC = env('EXNODE_PUBLIC')
EXNODE_PRIVATE = env('EXNODE_PRIVATE')
IP_ADDRESS = env('IP_ADDRESS')
MERCHANT_ID = env('MERCHANT_ID')
ExNode = ExNodeClient(EXNODE_PUBLIC, EXNODE_PRIVATE)
