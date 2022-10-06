from .base import * # NOQA
#NOQA告知PEP8 规范检测工具不需要检测

DEBUG=True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}