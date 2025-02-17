import json
import logging
from dataclasses import dataclass, field
from typing import Callable, TypeVar, Any

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from environs import Env

from service.TGClient import TG_Acc, TGClient_S
# from service.exnode import ExNodeClient

logger = logging.getLogger(__name__)
env = Env()
env.read_env()

bot_token = env('BOT_TOKEN')
link_support = env('LINK_SUPPORT')

dp = Dispatcher()
bot = Bot(bot_token)
BOT_ID = bot.id
link_to_bot = "https://t.me/best_acc_seller_bot"
USERNAME_BOT = "@best_acc_seller_bot"
path_to_logo = "data/main.jpg"
session_path = env('SESSION_PATH')
api_id = int(env('API_ID'))
api_hash = env('API_HASH')
phone_number = env('PHONE_NUMBER')
SQLALCHEMY_DATABASE_URI = f'sqlite+aiosqlite:///data/database.db'
CONFIG_FILE = "data/config.json"
tg_acc = TG_Acc(session_name=session_path, api_id=api_id, api_hash=api_hash, phone_number=phone_number)
client_s = TGClient_S(tg_acc)
LIMIT_PRICE = 5.0
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
EXCEL_TEMPLATE_PATH_REPLACE_CHANGE = "service/Excel/template.xlsx"
EXCEL_TEMPLATE_PATH_DELETE = "service/Excel/template_del.xlsx"
EXCEL_LOAD_FILE_PATH = "service/Excel"
USERNAME = env("USERNAME")

EXNODE_PUBLIC = env('EXNODE_PUBLIC')
EXNODE_PRIVATE = env('EXNODE_PRIVATE')
IP_ADDRESS = env('IP_ADDRESS')
MERCHANT_ID = env('MERCHANT_ID')
# ExNode = ExNodeClient(EXNODE_PUBLIC, EXNODE_PRIVATE)

LOCAL_HOST = env("LOCAL_HOST")
LOCAL_PORT = int(env("LOCAL_PORT"))
NAME_SHOP = "accounts"

API_HOST = env("API_HOST")
API_PORT = int(env("API_PORT"))
SECRET_KEY = env("SECRET_KEY")
