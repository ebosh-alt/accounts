from aiogram import Dispatcher, Bot
from environs import Env

env = Env()
env.read_env()

api_key = env('BOT_TOKEN')
link_support = env('LINK_SUPPORT')
dp = Dispatcher()
bot = Bot(api_key, parse_mode="Markdown")

