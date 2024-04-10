from aiogram import Dispatcher, Bot
from environs import Env
from service.TGClient import TG_Acc, TGClient_S

env = Env()
env.read_env()

api_key = env('BOT_TOKEN')
dp = Dispatcher()
bot = Bot(api_key, parse_mode="Markdown")
link_to_bot = "https://t.me/selling_accounts_test_bot"

session_path = env('SESSION_PATH')
api_id = int(env('API_ID'))
api_hash = env('API_HASH')
phone_number = env('PHONE_NUMBER')
tg_acc = TG_Acc(session_name=session_path, api_id=api_id, api_hash=api_hash, phone_number=phone_number)
client_s = TGClient_S(tg_acc)