from typing import Annotated, List

from pydantic import Field, field_validator
from pydantic_settings import SettingsConfigDict, BaseSettings, NoDecode

from data.settings.base import ConfigBase


class TelegramBotConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="tg_bot_")
    token: str
    link: str
    username: str


class DatabaseConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="db_")
    dbms: str
    driver: str
    user: str
    password: str
    host: str
    port: int
    name: str

    @property
    def link_connect(self):
        return f"{self.dbms}+{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class TelegramClientConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="tg_client_")
    session_path: str
    api_id: int
    api_hash: str
    phone_number: str


class ManagerConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="manager_")
    seller_id: int
    username: str
    link_support: str


class AdminConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="admin_")
    ids: Annotated[List[int], NoDecode]
    main_id: int

    @field_validator('ids', mode='before')
    def decode_numbers(cls, v: str) -> List[int]:
        return [int(x) for x in v.split(',')]



class ShopConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="shop_")
    base_percent: float
    percent_guarantor: float
    limit_price: float


class ExcelConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="excel_")
    template_path: str
    load_file_path: str


class ExnodeConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="exnode_")
    public_key: str
    private_key: str
    merchant_id: str


class ServerConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="server_")
    host: str
    port: int


class FastApiConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="fast_api_")
    host: str
    port: int
    private_key: str


class Config(BaseSettings):
    telegram_bot: TelegramBotConfig = Field(default_factory=TelegramBotConfig)
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    telegram_client: TelegramClientConfig = Field(default_factory=TelegramClientConfig)
    manager: ManagerConfig = Field(default_factory=ManagerConfig)
    admin: AdminConfig = Field(default_factory=AdminConfig)
    shop: ShopConfig = Field(default_factory=ShopConfig)
    excel: ExcelConfig = Field(default_factory=ExcelConfig)
    exnode: ExnodeConfig = Field(default_factory=ExnodeConfig)
    server: ServerConfig = Field(default_factory=ServerConfig)
    fastapi: FastApiConfig = Field(default_factory=FastApiConfig)

    @classmethod
    def load(cls) -> "Config":
        return cls()
