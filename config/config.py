import logging
from config.settings.setting import Config


logger = logging.getLogger(__name__)

config: Config = Config.load()

logger.info(config.db)
logger.info(config.admin)