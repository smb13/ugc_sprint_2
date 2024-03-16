"""
For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import environ
from split_settings.tools import include

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=str,
)  # set default values and casting

environ.Env.read_env(".env")

include(
    "components/base.py",
    "components/apps.py",
    "components/middlewares.py",
    "components/templates.py",
    "components/databases.py",
    "components/auth.py",
)
