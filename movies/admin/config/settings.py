"""
For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
import logging

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

import environ
from split_settings.tools import include

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=str,
)  # set default values and casting

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

environ.Env.read_env(".env")

include(
    "components/base.py",
    "components/apps.py",
    "components/middlewares.py",
    "components/templates.py",
    "components/databases.py",
    "components/auth.py",
)
