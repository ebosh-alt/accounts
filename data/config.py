import json
import logging
from dataclasses import dataclass, field
from typing import Callable, TypeVar, Any

from aiogram import Dispatcher, Bot
from environs import Env

from service.TGClient import TG_Acc, TGClient_S
from service.exnode import ExNodeClient

logger = logging.getLogger(__name__)
env = Env()
env.read_env()

bot_token = env('BOT_TOKEN')
link_support = env('LINK_SUPPORT')

dp = Dispatcher()
bot = Bot(bot_token)
# bot = Bot(bot_token, parse_mode=ParseMode.MARKDOWN_V2)
BOT_ID = bot.id
link_to_bot = "https://t.me/Sale_of_account_bot"
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
EXCEL_TEMPLATE_PATH = env('EXCEL_TEMPLATE_PATH')
EXCEL_LOAD_FILE_PATH = env('EXCEL_LOAD_FILE_PATH')
USERNAME = env("USERNAME")

EXNODE_PUBLIC = env('EXNODE_PUBLIC')
EXNODE_PRIVATE = env('EXNODE_PRIVATE')
IP_ADDRESS = env('IP_ADDRESS')
MERCHANT_ID = env('MERCHANT_ID')
ExNode = ExNodeClient(EXNODE_PUBLIC, EXNODE_PRIVATE)


@dataclass
class Config:
    """Класс для работы с конфигурацией."""
    name_shop: str = ""
    description_seller: str = ""
    acceptable_account_types: list = field(default_factory=list)

    def __post_init__(self) -> None:
        """Загружает конфигурацию из файла при инициализации экземпляра."""
        config_data = self.load_config()
        if config_data:  # Загружаем данные, если файл существует и не пустой
            self.set_config(config_data)

    def set_config(self, config_data: dict[str, Any]) -> None:
        self.name_shop = config_data.get('name_shop', self.name_shop)
        self.description_seller = config_data.get('description_seller', self.description_seller)
        self.acceptable_account_types = config_data.get('acceptable_account_types', self.acceptable_account_types)

    def save_config(self) -> None:
        """Сохраняет обновленные параметры в конфигурационный файл."""
        config_json = {
            "name_shop": self.name_shop,
            "description_seller": self.description_seller,
            "acceptable_account_types": self.acceptable_account_types,
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config_json, f, indent=4)

    @staticmethod
    def load_config() -> dict | None:
        """Загружает параметры конфигурации из файла, если файл существует."""
        try:
            with open(CONFIG_FILE, 'r') as f:
                config_json = json.load(f)
                return config_json
        except FileNotFoundError:
            logger.info(f"Файл конфигурации '{CONFIG_FILE}' не найден. Используются значения по умолчанию.")
            return None
        except json.JSONDecodeError:
            logger.info("Ошибка чтения конфигурационного файла. Проверьте его формат.")
            return None
