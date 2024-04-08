from aiogram import Dispatcher, Bot
from environs import Env

env = Env()
env.read_env()

api_key = env('BOT_TOKEN')
dp = Dispatcher()
bot = Bot(api_key, parse_mode="Markdown")
link_to_bot = "https://t.me/selling_accounts_test_bot"
