import logging
import os

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from core.config import settings

# Инициализация Sentry SDK если есть env SENTRY_DSN
if SENTRY_DSN := os.getenv("SENTRY_DSN"):

    sentry_logging = LoggingIntegration(
        level=logging.WARNING,  # Захват логов уровня WARNING и выше
        event_level=logging.ERROR  # Отправка событий в Sentry начиная с уровня ERROR
    )

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[sentry_logging],
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

# Базовая конфигурация логгирования
logger = logging.getLogger("etl_logger")
logger.setLevel(settings.logger.log_level)

# Настойки логов для вывода в консоль
terminal = logging.StreamHandler()
format_terminal = logging.Formatter(settings.logger.log_format)
terminal.setFormatter(format_terminal)
logger.addHandler(terminal)
