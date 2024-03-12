import logging

from core.config import settings

# Базовая конфигурация логгирования
logger = logging.getLogger("etl_logger")
logger.setLevel(settings.logger.log_level)

# Настойки логов для вывода в консоль
terminal = logging.StreamHandler()
format_terminal = logging.Formatter(settings.logger.log_format, datefmt="[%Y-%m-%d %H:%M:%S %z]")
terminal.setFormatter(format_terminal)
logger.addHandler(terminal)
