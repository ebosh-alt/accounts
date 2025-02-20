import logging

from .settings.setting import Config

logger = logging.getLogger(__name__)

config: Config = Config.load()